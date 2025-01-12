import time
import numpy as np
import pygad
from typing import Any, Optional

from src.python.io import parser_excel
from src.python.api import api
from src.python.api.models.date import Date
from src.python.api.models.day import Day
from src.python.api.models.event import Event
from src.python.api.models.priority import Priority
from src.python.api.models.room import Room
from src.python.api.models.time_slot import TimeSlot
from src.python.api.models.course import Course
from src.python.api.models.semester import Semester
from src.python.db.database import Database
from src.python.log.logger import logger_ga

from src.python.ga.constraints import (
    fitness_function, evaluate_constraints_core, evaluate_constraints_hard,
)

HARD_CONSTRAINT: int = 100
MID_CONSTRAINT: int = 3

NUM_GENERATIONS: int = 20000
SOL_PER_POP: int = 300


def prepare(
    term: str,
) -> tuple[
    list[Event],
    list[tuple[tuple[int, Date], tuple[int, Room]]],
    dict[tuple[int, int], Priority],
]:
    """Prepares all structures filled with data from the database.

    Args:
        term: Term for preparing the data, either "Sommer" or "Winter".

    Returns:
        A tuple containing the following elements:
        lessons: List of events, in which each event appears n times where n is the number of weekly
            hours of the event.
        date_x_room: List of pairs of pairs ((date id, date), (room id, room)).
        employee_dislikes_date: Dictionary of pairs (employee id, date id) to priorities.
    """
    lessons: list[Event] = [
        event
        for event in api.get_events_by_id().values()
            if event.term.name == term
                for _ in range(event.weekly_blocks)
    ]

    logger_ga.debug(f"Prepared lessons count: {len(lessons)}")

    date_x_room: list[tuple[tuple[int, Date], tuple[int, Room]]] = [
        (d, r)
        for d in api.get_dates_by_id().items()
        for r in api.get_rooms_by_id().items()
    ]
    priorities_by_id: dict[int, Priority] = api.get_priorities_by_id()
    employee_dislikes_date: dict[tuple[int, int], Priority] = {
        (employee_id, date_id): priorities_by_id[priority_id]
        for (
            employee_id,
            date_id,
        ), priority_id in api.get_employee_dislikes_date().items()
    }
    return lessons, date_x_room, employee_dislikes_date


def genetic_algorithm(generations: int = NUM_GENERATIONS, term: str = "Sommer"):
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
    logger_ga.info(f"Starting genetic algorithm for term {term} with {generations} generations")
    lessons, date_x_room, employee_dislikes_date = prepare(term)
    logger_ga.info(f"Data preparation complete.")

    def parse_pygad_solution_for_print(
        pygad_solution: list[np.uint16],
    ) -> dict[str, Any]:
        """Parses a PyGad solution for printing and transforms it into a human-readable format.

        It consists of multiple layers:
        - The first layer contains the days of the week.
            - Within each day of the week, all existing time slots are placed.
                - Each time slot stores the rooms and associated events.

        An example might be the following:

        {
            "Montag": {
                "08:00 - 09:15": {
                    "Audimax": {
                        "Analysis": {
                            "B_Inf" : [1 , 2],
                            ...
                        }
                    }
                },
                "09:30 - 10:45": {
                    "Hörsaal 4": {
                        "Diskrete Mathematik": {
                            "B_Inf" : [1 , 2],
                                ...
                            }
                        }
                    }
                }
            },
            "Dienstag": {
                ...
            },
            ...
        }

        Args:
            pygad_solution: PyGad solution to parse.

        Returns:
            A dictionary parsed from the PyGad solution.
        """
        courses_by_id: dict[int, Course] = api.get_courses_by_id()
        semesters_by_id: dict[int, Semester] = api.get_semesters_by_id()
        result: dict[str, Any] = {}
        for i, date_x_room_id in enumerate(pygad_solution):
            (_, date), (_, room) = date_x_room[date_x_room_id]
            day: Day = date.day
            time_slot: TimeSlot = date.time_slot
            time: str = (
                time_slot.start_time.strftime("%H:%M")
                + " - "
                + time_slot.end_time.strftime("%H:%M")
            )
            event: Event = lessons[i]  # type: ignore
            if day.name not in result:
                result[day.name] = {}
            if time not in result[day.name]:
                result[day.name][time] = {}
            event_name = event.name
            count_event_at_time = 1
            while event_name in result[day.name][time]:
                event_name = f"{event.name} ({count_event_at_time})"
                count_event_at_time += 1
            result[day.name][time][event_name] = {}
            result[day.name][time][event_name][room.name] = {
                courses_by_id[course_id].abbreviation: [
                    semesters_by_id[semester_id].value for semester_id in semesters_ids
                ]
                for course_id, semesters_ids in event.participants.items()
            }
        return result

    def on_generation(instance: pygad.GA):
        """Callback to log constraint violations of the best solution after each generation."""
        best_solution, fitness, _ = instance.best_solution()  # type: ignore
        lessons, date_x_room, employee_dislikes_date = instance.variables  # type: ignore

        _, violated_core, _ = evaluate_constraints_core(best_solution, lessons, date_x_room)
        _, violated_hard, _ = evaluate_constraints_hard(best_solution, lessons, date_x_room, employee_dislikes_date)
        _, violated_soft, _ = evaluate_constraints_core(best_solution, lessons, date_x_room)

        logger_ga.info(f"Generation {instance.generations_completed} with Fitness {fitness}")
        logger_ga.info(f"Core Constraints conflicts: {violated_core}")
        logger_ga.info(f"Hard Constraints conflicts: {violated_hard}")
        logger_ga.info(f"Soft Constraints conflicts: {violated_soft}")

    ga_instance = pygad.GA(
        num_genes=len(lessons),
        gene_type=np.uint32,  # type: ignore
        gene_space={"low": 0, "high": len(date_x_room)},
        allow_duplicate_genes=False,
        fitness_func=fitness_function,
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
    ga_instance.variables = (lessons, date_x_room, employee_dislikes_date)  # type: ignore

    logger_ga.info("Running genetic algorithm...")
    start_time = time.perf_counter()
    ga_instance.run()
    runtime = time.perf_counter() - start_time
    logger_ga.info(f"Genetic algorithm completed in {runtime:.2f} seconds")

    best_solution = ga_instance.best_solution()
    logger_ga.info(f"Best fitness: {best_solution[1]}")  # type: ignore

    parsed_solution = parse_pygad_solution_for_print(best_solution[0])  # type: ignore
    return runtime, parsed_solution, best_solution[1], ga_instance.generations_completed


def main() -> None:
    Database().initialize(delete_database_file=True)
    parser_excel.parse()
    runtime, parsed_solution, fitness, generations_completed = genetic_algorithm()


if __name__ == "__main__":
    main()
