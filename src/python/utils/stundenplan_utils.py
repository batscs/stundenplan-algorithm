from typing import List, Any, Dict

import numpy as np

from src.python.ga import evaluator


def verify_input(data):
    return {
        "success": True
    }


def parse_solution_into_timetable(
        pygad_solution,
        date_x_room,
        lessons
) -> List[Dict[str, Any]]:
    """Parses a PyGad solution for printing and transforms it into a human-readable list format.

    Args:
        pygad_solution: PyGad solution to parse.
        date_x_room: List of date and room pairs.
        lessons: List of lesson dictionaries.

    Returns:
        A list of dictionaries, each representing a scheduled event.
    """
    timetable = []

    for i, date_x_room_id in enumerate(pygad_solution):
        schedule = date_x_room[date_x_room_id]
        date = schedule["date"]
        room = schedule["room"]
        event = lessons[i]  # type: ignore

        day = date['day']
        timeslot = date['timeslot']
        event_name = event["name"]
        room_name = room["name"]
        participants = event["participants"]

        # Check for duplicate events in the same timeslot and room
        existing_event = next(
            (item for item in timetable if item["day"] == day and
             item["timeslot"] == timeslot and
             item["event"].startswith(event_name)),
            None
        )

        if existing_event:
            # If the event already exists in the same timeslot, append a suffix
            count = sum(1 for item in timetable if item["day"] == day and
                        item["timeslot"] == timeslot and
                        item["event"].startswith(event_name))
            event_entry = {
                "day": day,
                "timeslot": timeslot,
                "event": f"{event_name} ({count})",
                "room": room_name,
                "participants": participants
            }
        else:
            event_entry = {
                "day": day,
                "timeslot": timeslot,
                "event": event_name,
                "room": room_name,
                "participants": participants
            }

        timetable.append(event_entry)

    return timetable


def parse_solution_for_print(best_solution, fitness, date_x_room, lessons):
    result = {}

    timetable = parse_solution_into_timetable(best_solution, date_x_room, lessons)  # type: ignore

    core_fitness, core_unsatisfied, core_satisfied = (
        evaluator.evaluate_constraints_core(best_solution, lessons, date_x_room))

    hard_fitness, hard_unsatisfied, hard_satisfied = (
        evaluator.evaluate_constraints_hard(best_solution, lessons, date_x_room))

    soft_fitness, soft_unsatisfied, soft_satisfied = (
        evaluator.evaluate_constraints_soft(best_solution, lessons, date_x_room))

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
