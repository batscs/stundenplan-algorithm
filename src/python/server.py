import fnmatch
import os
import threading
from datetime import datetime

import pytz
from flask import Flask, request, jsonify, send_from_directory, render_template_string, abort, Response
from flask_restx import Api, Resource, fields
from src.python.app import core, config
from src.python.app.docs import DocumentationCompiler
from src.python.io import reader_json, printer_json
from src.python.log.logger import logger_app, get_logs_algorithm, get_logs_application, logger_srv, get_logs_server
from src.python.utils import path_utils, stundenplan_utils
from src.python.utils.models import register_models
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__, static_folder=path_utils.PATH_SERVER_STATIC, static_url_path="/")
api = Api(app,
          title='Stundenplan API Documentation',
          description='Eine umfassende API-Dokumentation für den [Stundenplan-Algorithmus](/).',
          doc='/api/docs',
          prefix='/api',
          strict_slashes=False)

# Define namespaces
ns_config = api.namespace('config', description='Configuration operations')
ns_stundenplan = api.namespace('stundenplan', description='Stundenplan operations')
ns_status = api.namespace('status', description='Status operations')
ns_logs = api.namespace('logs', description='Log insights')

# Models for request and response validation
models = register_models(api)
model_config = models['config_model']
model_stundenplan_input = models['stundenplan_input']
model_stundenplan_output = models['stundenplan_output']
model_status = models['status_model']

# Global variables and lock
algorithm_lock = threading.Lock()
is_running = False

allowed_ips = config.get_server_allowed_ips()

compiler = DocumentationCompiler(path_utils.PATH_DOCS, recompile=True)

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    logger_srv.info(f"{client_ip} - {request.method} {request.path}")
    if not any(fnmatch.fnmatch(client_ip, pattern) for pattern in allowed_ips):
        logger_srv.warning(f"UNAUTHORIZED: {client_ip} - {request.method} {request.path}")
        abort(403)  # Zugriff verweigern


def run_genetic_algorithm_thread():
    global is_running

    try:
        core.run()
    except Exception as e:
        logger_app.error(f"Error during algorithm execution: {str(e)}")
    finally:
        is_running = False  # Reset the running flag


@ns_logs.route('/')
class LogsAlgorithmResource(Resource):

    @ns_config.doc('get_logs')
    def get(self):
        """Retrieves the available logs"""
        return ["application", "algorithm", "server"]


@ns_logs.route('/server')
class LogsAlgorithmResource(Resource):

    @ns_config.doc('get_server_logs')
    def get(self):
        """Retrieves the algorithm logs."""
        return Response(get_logs_server(), content_type="text/plain")

@ns_logs.route('/algorithm')
class LogsAlgorithmResource(Resource):

    @ns_config.doc('get_algorithm_logs')
    def get(self):
        """Retrieves the algorithm logs."""
        return Response(get_logs_algorithm(), content_type="text/plain")


@ns_logs.route('/application')
class LogsAlgorithmResource(Resource):

    @ns_config.doc('get_application_logs')
    def get(self):
        """Retrieves the application logs."""
        return Response(get_logs_application(), content_type="text/plain")


@ns_config.route('/')
class ConfigResource(Resource):

    @ns_config.doc('get_config')
    @ns_config.marshal_with(model_config, mask=False)
    def get(self):
        """Retrieves the current application configuration."""
        return config.get_config(), 200

    @ns_config.doc('post_config')
    @ns_config.expect(model_config)
    @ns_config.response(202, 'Accepted: Config changes have been applied if valid')
    def post(self):
        """Updates the application configuration with new data.

        This endpoint allows partial updates to the configuration. You can provide only the fields
        that need to be updated in the request body. If a field is omitted, it retains its current value."""
        data = request.get_json()
        config.set_config(data)
        return {"status": "Config changes have been applied"}, 202


@ns_stundenplan.route('/')
class StundenplanResource(Resource):

    @ns_stundenplan.doc('get_stundenplan')
    @ns_stundenplan.marshal_with(model_stundenplan_output, mask=False)
    @ns_config.response(200, 'OK: Returning Stundenplan Result')
    @ns_config.response(404, "Not Found: No Stundenplan Result has been generated yet")
    @ns_config.response(500, "Internal Server Error: Output File can't be parsed")
    def get(self):
        """Fetches the latest Stundenplan data from the server."""
        client_ip = request.remote_addr
        logger_srv.info(f"Attempting to get stundenplan-result from user {client_ip}")

        path = path_utils.RESOURCE_OUTPUT_PATH
        try:
            files = [f for f in os.listdir(path) if f.startswith("parsed_solution_") and f.endswith(".json")]

            newest_file = max(files, key=lambda f: os.path.getctime(os.path.join(path, f)))
            filepath = os.path.join(path, newest_file)
            logger_app.debug(f"Newest file determined: {filepath}")

            data = reader_json.parse(filepath)
            if data is None:
                logger_app.error(f"Attempted to get stundenplan-result from {client_ip}, but input data can't be parsed or is empty")
                return {
                    "data": None,
                    "timestamp": datetime.now().isoformat(),
                    "status": "failed"
                }, 500

            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "data": data
            }, 200
        except Exception as e:
            logger_app.error(f"Attempted to get stundenplan-result from {client_ip}, but no input data is available")
            return {
                "data": None,
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            }, 404

    @ns_stundenplan.doc('post_stundenplan')
    @ns_stundenplan.expect(model_stundenplan_input)
    @ns_stundenplan.response(201, "Accepted: Stundenplan data saved successfully.")
    @ns_stundenplan.response(400, "Bad Request: Missing or malformed input data.")
    @ns_stundenplan.response(409, "Conflict: The algorithm is currently running.")
    def post(self):
        """Saves Stundenplan data to the server. Input data is validated before saving."""
        global is_running

        client_ip = request.remote_addr
        logger_srv.info(f"Attempting to save new stundenplan-input data from user {client_ip}")

        if is_running:
            api.abort(409, "Cannot save data while algorithm is running")
            # TODO return irgendwas, 409

        current_time: str = (
            datetime.now(pytz.utc)
            .astimezone(pytz.timezone("Europe/Berlin"))
            .strftime("%Y-%m-%d_%H-%M-%S")
        )

        data = request.get_json()
        verify = stundenplan_utils.verify_input(data)

        if not verify["success"]:
            logger_app.warning("Attempted to load invalid data")
            logger_app.warning("Messages: " + str(verify["messages"]))

            filename = f"server_input_{current_time}_invalid.json"
            printer_json.save(data, config.get_path_input_custom(filename))

            return verify, 400

        filename = f"server_input_{current_time}.json"
        config.set_filename_input(filename)
        printer_json.save(data, config.get_path_input())

        return verify, 201

    @ns_stundenplan.doc('put_stundenplan')
    @ns_stundenplan.response(202, "Accepted: Stundenplan Generation has been started.")
    @ns_stundenplan.response(400, "Bad Request: Missing input data.")
    @ns_stundenplan.response(409, "Conflict: The algorithm is currently running.")
    def put(self):
        """Initiates the genetic algorithm to generate solutions for Stundenplan data."""
        global is_running
        client_ip = request.remote_addr
        logger_srv.info(f"Attempting to start algorithm from user {client_ip}")

        data = reader_json.parse(config.get_path_input())
        if data is None:
            api.abort(400, "No Stundenplan-Data exists")

        if is_running:
            api.abort(409, "An algorithm run is already in progress")

        try:
            with algorithm_lock:
                is_running = True
                threading.Thread(
                    target=run_genetic_algorithm_thread,
                    daemon=True
                ).start()
            return {"status": "Algorithm started"}, 202
        except Exception as e:
            api.abort(500, str(e))


@ns_status.route('/')
class StatusResource(Resource):
    @ns_status.doc('get_status')
    def get(self):
        """Checks the current status of the server and algorithm execution."""
        return {"is_running": is_running}, 200


# Serve the index.html
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/docs/<path:filename>")
def serve_file(filename):
    # Versuche, die Datei als kompiliertes Dokument zu laden
    doc_content = compiler.get_document(filename)
    if doc_content:
        return render_template_string(doc_content)

    # Falls nicht kompiliert, versuche sie als Rohdatei zu laden
    raw_file_response = compiler.serve_raw_file(filename)
    if raw_file_response:
        return raw_file_response

    # Wenn weder HTML noch Rohdatei gefunden wird, 404 zurückgeben
    return "File not found", 404

@app.route("/docs/")
def serve_docs_index():
    doc_content = compiler.get_document("index.html")
    if doc_content:
        return render_template_string(doc_content)
    return "Document not found", 404



if __name__ == "__main__":
    logger_app.debug("Starting Server")

    stundenplan_config = reader_json.parse(config.get_application_path_config())

    if stundenplan_config is not None:
        logger_app.debug("Loaded existing configuration file")
        stundenplan_config["application"]["filepath_input"] = "server_input.json"
    else:
        stundenplan_config = {
            "application": {
                "filepath_input": "server_input.json"
            }
        }

    config.set_config(stundenplan_config)

    app.run(host="0.0.0.0", port=1111)
