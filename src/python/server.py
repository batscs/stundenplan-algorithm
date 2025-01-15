import os
from datetime import datetime
from flask import Flask, request, jsonify
from src.python.app import core
from src.python.io import reader_json, printer_json
from src.python.app import config
from src.python.log.logger import logger_app
import threading
from src.python.utils import path_utils
from src.python.utils import stundenplan_utils

app = Flask(__name__)

# Global variables and lock
algorithm_lock = threading.Lock()
is_running = False

# TODO logger_server

# TODO /run geht nur einmal, danach nicht wegen sqlite database

# TODO /config POST und GET wäre auch praktisch, ähnlich zu logging_config.json

def run_genetic_algorithm_thread():
    global is_running

    try:
        core.run()

    except Exception as e:
        logger_app.error(f"Error during algorithm execution: {str(e)}")
    finally:
        is_running = False  # Reset the running flag


@app.route('/stundenplan', methods=['POST'])
def post_data():
    global is_running

    if is_running:
        return jsonify({"error": "Cannot save data while algorithm is running"}), 409

    data = request.get_json()

    verify = stundenplan_utils.verify_input(data)

    if not verify["success"]:
        return jsonify({"error": "Invalid input Data"}), 409

    path = config.get_path_input()
    printer_json.save(data, path)
    return jsonify({"status": "Data saved successfully"}), 201


@app.route('/stundenplan', methods=['GET'])
def get_data():
    path = path_utils.RESOURCE_OUTPUT_PATH

    try:
        # Find the newest output file with the expected naming pattern
        files = [f for f in os.listdir(path) if f.startswith("parsed_solution_") and f.endswith(".json")]
        if not files:
            logger_app.debug("No output files found in the directory.")
            return jsonify({"error": "No output files found"}), 404

        newest_file = max(files, key=lambda f: os.path.getctime(os.path.join(path, f)))
        filepath = os.path.join(path, newest_file)
        logger_app.debug(f"Newest file determined: {filepath}")

        # Parse the file
        data = reader_json.parse(filepath)
        if data is None:
            logger_app.error("Failed to parse the file or file is empty.")
            return jsonify({
                "status": "failed",
                "timestamp": datetime.now().isoformat(),
                "data": None
            }), 500

        # Return parsed data with additional metadata
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": data
        }), 200

    except Exception as e:
        logger_app.error(f"Error in /stundenplan-run: {str(e)}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/stundenplan-run', methods=['GET']) # TODO rename to /stundenplan and method = PATCH
def run_algorithm():
    global is_running

    data = reader_json.parse(config.get_path_input())

    if data is None:
        return jsonify({"error": "No Stundenplan-Data exists"}), 400

    if is_running:
        return jsonify({"error": "An algorithm run is already in progress"}), 409

    try:
        logger_app.debug("Incoming Request: Run Algorithm")

        # Start the genetic algorithm in a separate thread
        with algorithm_lock:
            is_running = True
            threading.Thread(
                target=run_genetic_algorithm_thread,
                daemon=True
            ).start()

        return jsonify({"status": "Algorithm started"}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/status', methods=['GET'])
def status():
    return jsonify({"is_running": is_running})


if __name__ == "__main__":
    logger_app.debug("Starting Server")

    stundenplan_config = reader_json.parse(config.get_path_config())
    config.set_config(stundenplan_config)

    server_config = {
        "input": {
            "filename": "server_input.json"
        }
    }

    config.set_config(server_config)

    app.run(host="0.0.0.0", port=80)
