import time
from typing import Any, List, Dict

import numpy as np
import pygad
from src.python.api import database
from src.python.ga import evaluator
from src.python.log.logger import logger_ga
from src.python.utils import stundenplan_utils

NUM_GENERATIONS: int = 20000
SOL_PER_POP: int = 300

def genetic_algorithm(generations: int = NUM_GENERATIONS):
    """Executes a genetic algorithm using PyGad to find the optimal scheduling of events for a given
    term.

    Args:
        generations: Number of generations for which the genetic algorithm should run, defaults to
            `NUM_GENERATIONS`.

    Returns:
        A tuple containing the following elements:
        runtime: Runtime of the algorithm in seconds.
        parsed_solution: Best solution parsed into a human-readable format.
        fitness: Fitness of the best solution.
        generations_completed: Number of generations completed by the algorithm.
    """
    lessons = database.get_lessons()
    date_x_room = database.get_date_x_room()

    logger_ga.info(f"Starting genetic algorithm with {generations} generations")

    def on_generation(instance: pygad.GA):
        """Callback to log constraint violations of the best solution after each generation."""
        nonlocal best_solution_g, fitness_g
        best_solution_g, fitness_g, _ = instance.best_solution()  # type: ignore

        _, violated_core, _ = evaluator.evaluate_constraints_core(best_solution_g, lessons, date_x_room)
        _, violated_hard, _ = evaluator.evaluate_constraints_hard(best_solution_g, lessons, date_x_room)
        _, violated_soft, _ = evaluator.evaluate_constraints_soft(best_solution_g, lessons, date_x_room)

        logger_ga.info("----------------------------------------------------------")
        logger_ga.info(f"Generation {instance.generations_completed} with Best Fitness {fitness_g}")
        logger_ga.info(f"Core Constraints conflicts: {violated_core}")
        logger_ga.info(f"Hard Constraints conflicts: {violated_hard}")
        logger_ga.info(f"Soft Constraints conflicts: {violated_soft}")

    # sometimes inconsistencies occur, because on_generation has a different best_solution
    # than the best_solution being found here
    best_solution_g = None
    fitness_g = None

    ga_instance = pygad.GA(
        num_genes=len(lessons),
        gene_type=np.uint32,  # type: ignore
        gene_space={"low": 0, "high": len(date_x_room)},
        allow_duplicate_genes=False,
        fitness_func=evaluator.fitness_function,
        num_generations=generations,
        sol_per_pop=SOL_PER_POP,
        mutation_type="adaptive",
        mutation_probability=(0.1, 0.01),
        num_parents_mating=10,
        parent_selection_type="tournament",
        K_tournament=30,
        crossover_type="scattered",
        stop_criteria="reach_0",
        keep_elitism=1,
        random_seed=None,
        suppress_warnings=True,
        on_generation=on_generation,  # Add callback here
    )
    ga_instance.variables = (lessons, date_x_room)  # type: ignore

    logger_ga.info("Running genetic algorithm...")
    start_time = time.perf_counter()
    ga_instance.run()
    runtime = time.perf_counter() - start_time
    logger_ga.info(f"Genetic algorithm completed in {runtime:.2f} seconds")

    logger_ga.info(f"Best fitness: {fitness_g}")  # type: ignore

    # ----------
    result = stundenplan_utils.parse_solution_for_print(best_solution_g, fitness_g, date_x_room, lessons)

    return runtime, result, fitness_g, ga_instance.generations_completed
