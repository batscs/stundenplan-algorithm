from flask import Flask, request, jsonify
from db.database import Database
from utils import time_utils
from src.python.ga.genetic_algorithm import genetic_algorithm
from src.python.io import parser_json as parser
from src.python.io import printer_json as printer
from src.python.utils import path_utils
from src.python.log.logger import logger_app
import threading

app = Flask(__name__)

# Global variables and lock
algorithm_lock = threading.Lock()
is_running = False

# TODO logger_server

# TODO /run geht nur einmal, danach nicht wegen sqlite database

# TODO /config POST und GET wäre auch praktisch, ähnlich zu logging_config.json

def run_genetic_algorithm_thread(generations, term, output_format, debug_mode):
    global is_running

    try:
        logger_app.debug("Running Genetic Algorithm in a separate thread")
        Database().initialize(delete_database_file=True)
        parser.parse()

        print(f"Genetic algorithm started (generations = {generations}, term = {term})")

        runtime, parsed_solution, fitness, generations_completed = genetic_algorithm(generations, term)

        print(f"\nSolution fitness: {fitness}")
        print(f"Generations completed: {generations_completed}")
        print(f"Actual runtime: {time_utils.seconds_to_formatted_duration(runtime)}")

        printer.printer_save(parsed_solution, fitness, debug_mode)

    except Exception as e:
        logger_app.error(f"Error during algorithm execution: {str(e)}")
    finally:
        is_running = False  # Reset the running flag


@app.route('/run', methods=['GET'])
def run_algorithm():
    global is_running

    if is_running:
        return jsonify({"error": "An algorithm run is already in progress"}), 409

    try:
        logger_app.debug("Incoming Request: Run Algorithm")
        generations = 10
        term = "Winter"
        output_format = "Tabular"
        debug_mode = False

        # Start the genetic algorithm in a separate thread
        with algorithm_lock:
            is_running = True
            threading.Thread(
                target=run_genetic_algorithm_thread,
                args=(generations, term, output_format, debug_mode),
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
    app.run(host="0.0.0.0", port=80)
