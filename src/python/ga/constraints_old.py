import numpy as np
from typing import Optional, Any, Dict, Tuple, List, Set
from numpy.typing import NDArray

HARD_CONSTRAINT: int = 100

# TODO signature of functions probably need to be changed later to work with more customizable constraints

def evaluate_constraints_core(
    solution: NDArray[np.uint32],
    lessons: List,
    date_x_room: List[Tuple[Tuple[int, Any], Tuple[int, Any]]],
) -> Tuple[int, Dict[str, int], Dict[str, int]]:
    """
    Evaluates core constraints like overlaps for students, teachers, and rooms.
    Returns fitness, violations, and satisfied constraints.
    """
    fitness = 0
    constraint_violations = {
        "employee_conflicts": 0,
        "student_conflicts": 0,
        "room_capacity": 0,
        "room_type": 0,
    }
    constraints_satisfied = {
        "employee_conflicts": 0,
        "student_conflicts": 0,
        "room_capacity": 0,
        "room_type": 0,
    }
    employee_planned_at_date: Set[Tuple[int, int]] = set()
    date_x_students: Set[Tuple[int, int, int]] = set()

    for event_idx, date_x_room_id in enumerate(solution):
        event = lessons[event_idx]
        (date_id, date), (room_id, room) = date_x_room[date_x_room_id]

        # Check for employee conflicts
        for employee_id in event.employee_ids:
            employee_x_date = (employee_id, date_id)
            if employee_x_date in employee_planned_at_date:
                fitness += HARD_CONSTRAINT
                constraint_violations["employee_conflicts"] += 1
            else:
                constraints_satisfied["employee_conflicts"] += 1
            employee_planned_at_date.add(employee_x_date)

        # Check for student conflicts
        for course_id, semester_id in [
            (course_id, semester_id)
            for course_id, semester_ids in event.participants.items()
            for semester_id in semester_ids
        ]:
            date_x_student = (date_id, course_id, semester_id)
            if date_x_student in date_x_students:
                fitness += HARD_CONSTRAINT
                constraint_violations["student_conflicts"] += 1
            else:
                constraints_satisfied["student_conflicts"] += 1
            date_x_students.add(date_x_student)

        # Check for room capacity
        if room.participant_size < event.participant_size:
            fitness += HARD_CONSTRAINT
            constraint_violations["room_capacity"] += 1
        else:
            constraints_satisfied["room_capacity"] += 1

        # Check for room type
        if room.room_type != event.room_type:
            fitness += HARD_CONSTRAINT
            constraint_violations["room_type"] += 1
        else:
            constraints_satisfied["room_type"] += 1

    return fitness, constraint_violations, constraints_satisfied


def evaluate_constraints_hard(
    solution: NDArray[np.uint32],
    lessons: List,
    date_x_room,
    employee_dislikes_date,
) -> Tuple:
    """
    Evaluates hard constraints like disallowed days for events and employee preferences.
    Returns fitness, violations, and satisfied constraints.
    """
    fitness = 0
    constraint_violations = {
        "disallowed_days": 0,
        "employee_dislikes": 0,
    }
    constraints_satisfied = {
        "disallowed_days": 0,
        "employee_dislikes": 0,
    }

    for event_idx, date_x_room_id in enumerate(solution):
        event = lessons[event_idx]
        (date_id, date), (_, _) = date_x_room[date_x_room_id]

        # Check for disallowed days
        if date.day in event.disallowed_days:
            fitness += HARD_CONSTRAINT
            constraint_violations["disallowed_days"] += 1
        else:
            constraints_satisfied["disallowed_days"] += 1

        # Check for employee dislikes
        for employee_id in event.employee_ids:
            employee_x_date = (employee_id, date_id)
            priority = employee_dislikes_date.get(employee_x_date)
            if priority:
                fitness += priority.value
                constraint_violations["employee_dislikes"] += 1
            else:
                constraints_satisfied["employee_dislikes"] += 1

    return fitness, constraint_violations, constraints_satisfied


def evaluate_constraints_soft() -> Tuple[int, Dict[str, int], Dict[str, int]]:
    """
    Placeholder for soft constraint evaluation.
    """
    fitness = 0
    constraint_violations = {}
    constraints_satisfied = {}
    # Add logic for soft constraints in the future
    return fitness, constraint_violations, constraints_satisfied


def fitness_function(
    instance: Any, solution: NDArray[np.uint32], solution_idx: int
) -> int:
    """Fitness function to evaluate individual solutions."""
    lessons, date_x_room, employee_dislikes_date = instance.variables  # type: ignore

    # Evaluate core constraints
    core_fitness, core_violations, core_satisfied = evaluate_constraints_core(
        solution, lessons, date_x_room
    )

    # Evaluate hard constraints
    hard_fitness, hard_violations, hard_satisfied = evaluate_constraints_hard(
        solution, lessons, date_x_room, employee_dislikes_date
    )

    # Evaluate soft constraints
    soft_fitness, soft_violations, soft_satisfied = evaluate_constraints_soft()

    # Combine results
    total_fitness = core_fitness + hard_fitness + soft_fitness
    total_violations = {**core_violations, **hard_violations, **soft_violations}
    total_satisfied = {**core_satisfied, **hard_satisfied, **soft_satisfied}

    return -total_fitness
