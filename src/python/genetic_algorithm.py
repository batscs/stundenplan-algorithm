import time
import numpy as np
import pygad
from numpy.typing import NDArray
from typing import Any, Optional

import excel_parser
from api import api
from api.models.date import Date
from api.models.day import Day
from api.models.event import Event
from api.models.priority import Priority
from api.models.room import Room
from api.models.time_slot import TimeSlot
from api.models.course import Course
from api.models.semester import Semester
from db.database import Database
from log import logging_config

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


def fitness_function(
    instance: pygad.GA, solution: NDArray[np.uint32], solution_idx: int
) -> int:
    """Fitness function that evaluates individual solutions.

    The higher the fitness, the better the solution, with `fitness == 0` indicating an optimal
    solution.

    The solutions are represented within PyGad as integer arrays where the position in the array
    corresponds to a lecture unit, and the values correspond to a room-time pair. This creates a
    mapping from lecture unit -> (timeslot, room).

    Args:
        instance: PyGad instance using the fitness_function, which holds the necessary data
            structures for the calculation.
        solution: Solution for which the fitness is to be calculated.
        solution_idx: Index of the solution in the current generation (currently not used).

    Returns:
        Fitness of the solution.
    """
    lessons, date_x_room, employee_dislikes_date = (
        instance.variables  # type: ignore Variables is a tuple set by us, which is not a regular member of the instance.
    )
    fitness: int = 0
    employee_planned_at_date: set[tuple[int, int]] = set()
    date_x_students: set[tuple[int, int, int]] = set()
    for event, date_x_room_id in zip(lessons, solution):
        (date_id, date), (room_id, room) = date_x_room[date_x_room_id]
        # Check if date matches the event.
        if date.day in event.disallowed_days:
            fitness += HARD_CONSTRAINT
        for employee_id in event.employee_ids:
            # Check if employee already has an event scheduled at this date.
            employee_x_date: tuple[int, int] = (employee_id, date_id)
            if employee_x_date in employee_planned_at_date:
                fitness += HARD_CONSTRAINT
            employee_planned_at_date.add(employee_x_date)
            # Check if employee dislikes this date.
            priority: Optional[Priority] = employee_dislikes_date.get(employee_x_date)
            if priority is not None:
                fitness += priority.value
        # Check if room fits to estimated participant size.
        if room.participant_size < event.participant_size:
            fitness += HARD_CONSTRAINT
        # Check if room fits to the one required by the event.
        if room.room_type != event.room_type:
            fitness += HARD_CONSTRAINT
        # Check if students would have to participate in multiple events at the same time.
        for course_id, semester_id in [
            (course_id, semester_id)
            for course_id, semester_ids in event.participants.items()
            for semester_id in semester_ids
        ]:
            date_x_student = (date_id, course_id, semester_id)
            if date_x_student in date_x_students:
                fitness += HARD_CONSTRAINT
            date_x_students.add(date_x_student)
    return -fitness


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
    lessons, date_x_room, employee_dislikes_date = prepare(term)

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

    gene_space: dict[str, int] = {"low": 0, "high": len(date_x_room)}
    # Initialize and run genetic algorithm.
    ga_instance = pygad.GA(
        num_genes=len(lessons),
        gene_type=np.uint32,  # type: ignore
        gene_space=gene_space,
        allow_duplicate_genes=False,
        fitness_func=fitness_function,
        # "save_solutions":True,
        # Instance Size
        num_generations=generations,
        sol_per_pop=SOL_PER_POP,
        # Mutation
        mutation_type="adaptive",
        mutation_probability=(0.1, 0.01),
        # Parent Selection
        num_parents_mating=10,
        parent_selection_type="tournament",
        K_tournament=30,
        # Crossover
        crossover_type="scattered",
        # crossover_probability=0.5,
        stop_criteria="reach_0",
        keep_elitism=1,
        random_seed=0,
        suppress_warnings=True,
    )
    ga_instance.variables = (  # type: ignore Variables is a tuple set by us, which is not a regular member of the instance.
        lessons,
        date_x_room,
        employee_dislikes_date,
    )
    runtime: float = time.perf_counter()
    ga_instance.run()
    runtime = time.perf_counter() - runtime
    best_solution = ga_instance.best_solution()
    parsed_solution: dict[str, Any] = parse_pygad_solution_for_print(best_solution[0])  # type: ignore
    fitness: int = best_solution[1]  # type: ignore
    # ga_instance.plot_fitness()
    return runtime, parsed_solution, fitness, ga_instance.generations_completed


def main() -> None:
    logging_config.configure_logging()
    Database().initialize(delete_database_file=True)
    excel_parser.parse()
    runtime, parsed_solution, fitness, generations_completed = genetic_algorithm()


if __name__ == "__main__":
    main()
