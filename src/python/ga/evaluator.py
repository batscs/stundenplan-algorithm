import numpy as np
from typing import Optional, Any, Dict, Tuple, List, Set
from numpy.typing import NDArray

from src.python.api import database
from src.python.ga import evaluator_constraint

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

        # event = {name: string, employees: [string], participants: [string], size: integer, weekly_blocks: integer, room_type: string}
        # date = {day: integer, timeslot: integer}
        # room = {name: string, capacity: integer, room_type: string}

        # Check for employee conflicts
        for employee_id in event["employees"]:
            employee_x_date = (employee_id, date_id)
            if employee_x_date in employee_planned_at_date:
                constraint_violations["employee_conflicts"] += 1
            else:
                constraints_satisfied["employee_conflicts"] += 1
            employee_planned_at_date.add(employee_x_date)

        # Check for student conflicts
        for participant in event["participants"]:
            date_x_student = (date_id, participant)
            if date_x_student in date_x_students:
                constraint_violations["student_conflicts"] += 1
            else:
                constraints_satisfied["student_conflicts"] += 1
            date_x_students.add(date_x_student)

        if room["capacity"] < event["size"]:
            constraint_violations["room_capacity"] += 1
        else:
            constraints_satisfied["room_capacity"] += 1

        # Check for room type
        if room["room_type"] != event["room_type"]:
            constraint_violations["room_type"] += 1
        else:
            constraints_satisfied["room_type"] += 1

    fitness = -sum(constraint_violations.values())

    return fitness, constraint_violations, constraints_satisfied

def evaluate_constraint(constraint, solution, lessons, date_x_room):
    type = constraint["type"]

    if type == "EmployeeFreeTimeslots":
        return evaluator_constraint.evaluate_employee_free_timeslots(constraint, solution, lessons, date_x_room)
    elif type == "EmployeeSubsequentTimeslots":
        return evaluator_constraint.evaluate_employee_subsequent_timeslots(constraint, solution, lessons, date_x_room)
    elif type == "EventDistributeWeeklyBlocks":
        return evaluator_constraint.evaluate_event_distribute_weekly_blocks(constraint, solution, lessons, date_x_room)

    return 0

def evaluate_constraints_hard(solution: NDArray[np.uint32], lessons, date_x_room):
    violations = []
    satisfied = []
    total_fitness = 0

    constraints = database.get_constraints_hard()

    for constraint in constraints:
        fitness = evaluate_constraint(constraint, solution, lessons, date_x_room)
        if fitness == 0:
            satisfied.append(constraint)
        else:
            total_fitness += fitness
            violations.append(constraint)

    return total_fitness, violations, satisfied

def evaluate_constraints_soft(solution: NDArray[np.uint32], lessons, date_x_room):
    violations = []
    satisfied = []
    total_fitness = 0

    constraints = database.get_constraints_soft()

    for constraint in constraints:
        fitness = evaluate_constraint(constraint, solution, lessons, date_x_room)
        if fitness == 0:
            satisfied.append(constraint)
        else:
            total_fitness += fitness
            violations.append(constraint)

    return total_fitness, violations, satisfied

def fitness_function(
    instance: Any, solution: NDArray[np.uint32], solution_idx: int
) -> int:
    """Fitness function to evaluate individual solutions."""
    lessons, date_x_room = instance.variables  # type: ignore

    core_fitness, core_violations, core_satisfied = evaluate_constraints_core(solution, lessons, date_x_room)
    hard_fitness, hard_violations, hard_satisfied = evaluate_constraints_hard(solution, lessons, date_x_room)
    soft_fitness, soft_violations, soft_satisfied = evaluate_constraints_soft(solution, lessons, date_x_room)

    return core_fitness + hard_fitness + soft_fitness