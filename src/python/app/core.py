from src.python.api import database
from src.python.app import config
from src.python.ga import genetic_algorithm
from src.python.io import reader_json
from src.python.io import printer_json
from src.python.log.logger import logger_app
from src.python.utils import time_utils, stundenplan_utils


def run():
    input_data = reader_json.parse(config.get_path_input())

    if input_data is None:
        logger_app.error("Could not start core application, no input data exists")
        return

    verify = stundenplan_utils.verify_input(input_data)

    if not verify["success"]:
        logger_app.error("Could not start core application, invalid input data")
        logger_app.error("Messages: " + str(verify["messages"]))
        return

    database.inject(input_data)

    generations = config.get_algorithm_generations_max()
    logger_app.debug(f"Genetic algorithm started (generations = {generations})")

    runtime, parsed_solution, fitness, generations_completed = genetic_algorithm.genetic_algorithm(generations)
    logger_app.debug(f"Solution fitness: {fitness}")
    logger_app.debug(f"Generations completed: {generations_completed}")
    logger_app.debug(f"Actual runtime: {time_utils.seconds_to_formatted_duration(runtime)}")

    printer_json.save_solution(parsed_solution)