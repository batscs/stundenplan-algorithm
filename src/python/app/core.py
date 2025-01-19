from src.python.api import database
from src.python.app import config
from src.python.ga import genetic_algorithm
from src.python.io import reader_json
from src.python.io import printer_json
from src.python.utils import time_utils, stundenplan_utils


def run():
    input_data = reader_json.parse(config.get_path_input())

    if input_data is None:
        print("Error: Input File not found")
        return

    verify = stundenplan_utils.verify_input(input_data)

    if not verify["success"]:
        print("Error: Input Data invalid")
        return

    database.inject(input_data)

    generations = config.get_algorithm_generations_max()
    print(f"Genetic algorithm started (generations = {generations})")

    runtime, parsed_solution, fitness, generations_completed = genetic_algorithm.genetic_algorithm(generations)
    print(f"\nSolution fitness: {fitness}")
    print(f"Generations completed: {generations_completed}")
    print(f"Actual runtime: {time_utils.seconds_to_formatted_duration(runtime)}")

    printer_json.save_solution(parsed_solution)