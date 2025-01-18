import fnmatch
import os
import threading
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template_string, abort, Response
from flask_restx import Api, Resource, fields
from src.python.app import core, config
from src.python.app.docs import DocumentationCompiler
from src.python.io import reader_json, printer_json
from src.python.log.logger import logger_app, get_logs_algorithm, get_logs_application
from src.python.utils import path_utils, stundenplan_utils
from src.python.utils.models import register_models

app = Flask(__name__, static_folder=path_utils.PATH_SERVER_STATIC, static_url_path="/")
api = Api(app,
          title='Stundenplan API Documentation',
          description='Eine umfassende API-Dokumentation für das Stundenplan-System.',
          doc='/api/docs',
          prefix='/api')

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
    if not any(fnmatch.fnmatch(client_ip, pattern) for pattern in allowed_ips):
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
        return ["algorithm", "application"]


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
    def get(self):
        """Fetches the latest Stundenplan data from the server."""
        path = path_utils.RESOURCE_OUTPUT_PATH
        try:
            files = [f for f in os.listdir(path) if f.startswith("parsed_solution_") and f.endswith(".json")]
            if not files:
                logger_app.debug("No output files found in the directory.")
                api.abort(404, "No output files found")

            newest_file = max(files, key=lambda f: os.path.getctime(os.path.join(path, f)))
            filepath = os.path.join(path, newest_file)
            logger_app.debug(f"Newest file determined: {filepath}")

            data = reader_json.parse(filepath)
            if data is None:
                logger_app.error("Failed to parse the file or file is empty.")
                return {
                    "status": "failed",
                    "timestamp": datetime.now().isoformat(),
                    "data": None
                }, 500

            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "data": data
            }, 200
        except Exception as e:
            logger_app.error(f"Error in /stundenplan-run: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }, 500

    @ns_stundenplan.doc('post_stundenplan')
    @ns_stundenplan.expect(model_stundenplan_input)
    @ns_stundenplan.response(201, "Accepted: Stundenplan data saved successfully.")
    @ns_stundenplan.response(400, "Bad Request: Missing or malformed input data.")
    @ns_stundenplan.response(409, "Conflict: The algorithm is currently running.")
    def post(self):
        """Saves Stundenplan data to the server. Input data is validated before saving."""
        global is_running

        if is_running:
            api.abort(409, "Cannot save data while algorithm is running")

        data = request.get_json()
        verify = stundenplan_utils.verify_input(data)

        if not verify["success"]:
            api.abort(400, "Invalid input Data")

        path = config.get_path_input()
        printer_json.save(data, path)
        return {"status": "Data saved successfully"}, 201

    @ns_stundenplan.doc('patch_stundenplan')
    @ns_stundenplan.response(202, "Accepted: Stundenplan Generation has been started.")
    @ns_stundenplan.response(400, "Bad Request: Missing input data.")
    @ns_stundenplan.response(409, "Conflict: The algorithm is currently running.")
    def patch(self):
        """Initiates the genetic algorithm to generate solutions for Stundenplan data."""
        global is_running

        data = reader_json.parse(config.get_path_input())
        if data is None:
            api.abort(400, "No Stundenplan-Data exists")

        if is_running:
            api.abort(409, "An algorithm run is already in progress")

        try:
            logger_app.debug("Incoming Request: Run Algorithm")
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
def serve_doc(filename):
    doc_content = compiler.get_document(filename)
    if doc_content:
        return render_template_string(doc_content)
    return "Document not found", 404

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
        config.set_config(stundenplan_config)

    server_config = {
        "application": {
            "filepath_input": "server_input.json"
        }
    }

    config.set_config(server_config)

    app.run(host="0.0.0.0", port=80)
