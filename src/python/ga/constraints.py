import numpy as np
from typing import Optional, Any, Dict, Tuple, List, Set
from numpy.typing import NDArray

def evaluate_constraints_core(
    solution: NDArray[np.uint32],
    lessons,
    date_x_room
):
    """
    Evaluates core constraints like overlaps for students, teachers, and rooms.
    Returns fitness, violations, and satisfied constraints.
    """
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
    employee_planned_at_date = set()
    date_x_students = set()

    for event_idx, date_x_room_id in enumerate(solution):
        event = lessons[event_idx]
        (date_id, date), (room_id, room) = date_x_room[date_x_room_id]

        # Check for employee conflicts
        for employee_id in event["Employees"]:
            employee_x_date = (employee_id, date_id)
            if employee_x_date in employee_planned_at_date:
                constraint_violations["employee_conflicts"] += 1
            else:
                constraints_satisfied["employee_conflicts"] += 1
            employee_planned_at_date.add(employee_x_date)

        # Check for student conflicts
        for participant in event["Participants"]:
            date_x_student = (date_id, participant)
            if date_x_student in date_x_students:
                constraint_violations["student_conflicts"] += 1
            else:
                constraints_satisfied["student_conflicts"] += 1
            date_x_students.add(date_x_student)

        if room["Capacity"] < event["Participant Size"]:
            constraint_violations["room_capacity"] += 1
        else:
            constraints_satisfied["room_capacity"] += 1

        # Check for room type
        if room["Room Type"] != event["Room Type"]:
            constraint_violations["room_type"] += 1
        else:
            constraints_satisfied["room_type"] += 1

    fitness = -sum(constraint_violations.values())

    return fitness, constraint_violations, constraints_satisfied

def evaluate_constraints_hard(solution: NDArray[np.uint32], lessons, date_x_room):
    violations = []
    satisfied = []

    return 0, violations, satisfied

def evaluate_constraints_soft(solution: NDArray[np.uint32], lessons, date_x_room):
    violations = []
    satisfied = []

    return 0, violations, satisfied

def fitness_function(
    instance: Any, solution: NDArray[np.uint32], solution_idx: int
) -> int:
    """Fitness function to evaluate individual solutions."""
    lessons, date_x_room = instance.variables  # type: ignore

    core_fitness, core_violations, core_satisfied = evaluate_constraints_core(solution, lessons, date_x_room)

    return core_fitness