import time
from typing import Any

import numpy as np
import pygad
from src.python.api import api
from src.python.ga import constraints
from src.python.log.logger import logger_ga

NUM_GENERATIONS: int = 20000
SOL_PER_POP: int = 300


def prepare():
    """Prepares all structures filled with data from the database.

    Returns:
        A tuple containing the following elements:
        lessons: List of events, in which each event appears n times where n is the number of weekly
            hours of the event.
        date_x_room: List of pairs of pairs ((date id, date), (room id, room)).
        employee_dislikes_date: Dictionary of pairs (employee id, date id) to priorities.
    """

    lessons = [
        event
        for event in api.get_events_by_id()
                for _ in range(event["Weekly Blocks"])
    ]

    logger_ga.debug(f"Prepared lessons count: {len(lessons)}")

    date_x_room = [
        (d, r)
        for d in api.get_dates_by_id().items()
        for r in api.get_rooms_by_id().items()
    ]

    return lessons, date_x_room

def parse_solution_into_timetable(
    pygad_solution: list[np.uint16],
    date_x_room,
    lessons
) -> dict[str, Any]:
    """Parses a PyGad solution for printing and transforms it into a human-readable format.
    Args:
        pygad_solution: PyGad solution to parse.

    Returns:
        A dictionary parsed from the PyGad solution.
    """
    result = {}

    for i, date_x_room_id in enumerate(pygad_solution):
        (_, date), (_, room) = date_x_room[date_x_room_id]
        day =  f"day_{date['Day']}"
        timeslot = f"timeslot_{date['TimeSlot']}"
        event = lessons[i]  # type: ignore

        if day not in result:
            result[day] = {}
        if timeslot not in result[day]:
            result[day][timeslot] = {}

        event_name = event["Name"]
        count_event_at_time = 1

        while event_name in result[day][timeslot]:
            event_name = f"{event_name} ({count_event_at_time})"
            count_event_at_time += 1

        room_name = room["Name"]
        result[day][timeslot][event_name] = {
            "room": room_name,
            "participants": event["Participants"]
        }

    return result


def parse_solution_for_print(best_solution, fitness, date_x_room, lessons):
    result = {}

    timetable = parse_solution_into_timetable(best_solution, date_x_room, lessons)  # type: ignore

    core_fitness, core_unsatisfied, core_satisfied = (
        constraints.evaluate_constraints_core(best_solution, lessons, date_x_room))

    hard_fitness, hard_unsatisfied, hard_satisfied = (
        constraints.evaluate_constraints_hard(best_solution, lessons, date_x_room))

    soft_fitness, soft_unsatisfied, soft_satisfied = (
        constraints.evaluate_constraints_soft(best_solution, lessons, date_x_room))

    result["timetable"] = timetable
    result["metadata"] = {
        "fitness": fitness,
    }
    result["constraints"] = {
        "core": {
            "fitness": core_fitness,
            "unsatisfied": core_unsatisfied,
            "satisfied": core_satisfied,
        },
        "hard": {
            "fitness": hard_fitness,
            "unsatisfied": hard_unsatisfied,
            "satisfied": hard_satisfied,
        },
        "soft": {
            "fitness": soft_fitness,
            "unsatisfied": soft_unsatisfied,
            "satisfied": soft_satisfied,
        }
    }

    return result


def genetic_algorithm(generations: int = NUM_GENERATIONS):
    """Executes a genetic algorithm using PyGad to find the optimal scheduling of events for a given
    term.

    Args:
        generations: Number of generations for which the genetic algorithm should run, defaults to
            `NUM_GENERATIONS`.
        term: Term for which the schedule is being generated, defaults to "Sommer".

    Returns:
        A tuple containing the following elements:
        runtime: Runtime of the algorithm in seconds.
        parsed_solution: Best solution parsed into a human-readable format.
        fitness: Fitness of the best solution.
        generations_completed: Number of generations completed by the algorithm.
    """
    logger_ga.info(f"Starting genetic algorithm with {generations} generations")
    lessons, date_x_room = prepare()
    logger_ga.info(f"Data preparation complete.")

    def on_generation(instance: pygad.GA):
        """Callback to log constraint violations of the best solution after each generation."""
        best_solution, fitness, _ = instance.best_solution()  # type: ignore
        # lessons, date_x_room = instance.variables  # type: ignore

        _, violated_core, _ = constraints.evaluate_constraints_core(best_solution, lessons, date_x_room)
        # _, violated_hard, _ = evaluate_constraints_hard(best_solution, lessons, date_x_room)
        # _, violated_soft, _ = evaluate_constraints_soft()

        logger_ga.info(f"Generation {instance.generations_completed} with Fitness {fitness}")
        logger_ga.info(f"Core Constraints conflicts: {violated_core}")
        # logger_ga.info(f"Hard Constraints conflicts: {violated_hard}")
        # logger_ga.info(f"Soft Constraints conflicts: {violated_soft}")

    ga_instance = pygad.GA(
        num_genes=len(lessons),
        gene_type=np.uint32,  # type: ignore
        gene_space={"low": 0, "high": len(date_x_room)},
        allow_duplicate_genes=False,
        fitness_func=constraints.fitness_function,
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
        random_seed=0,
        suppress_warnings=True,
        on_generation=on_generation,  # Add callback here
    )
    ga_instance.variables = (lessons, date_x_room)  # type: ignore

    logger_ga.info("Running genetic algorithm...")
    start_time = time.perf_counter()
    ga_instance.run()
    runtime = time.perf_counter() - start_time
    logger_ga.info(f"Genetic algorithm completed in {runtime:.2f} seconds")

    best_solution, fitness, _ = ga_instance.best_solution()
    logger_ga.info(f"Best fitness: {fitness}")  # type: ignore

    # ----------
    result = parse_solution_for_print(best_solution, fitness, date_x_room, lessons)

    return runtime, result, fitness, ga_instance.generations_completed