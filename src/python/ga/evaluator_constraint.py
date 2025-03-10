def evaluate_employee_free_timeslots(constraint, solution, lessons, date_x_room):
    employee = constraint["owner"]
    timeslots = constraint["fields"]["timeslots"]
    inverted = constraint["inverted"]

    # timeslots is array of { day: integer, timeslot: integer }

    # if not inverted, employee is not allowed to have any event with him during any of those timeslots
    # if inverted, employee is only allowed to have events in given timeslots

    forbidden_slots = {(slot["day"], slot["timeslot"]) for slot in timeslots}
    violations = 0

    for event_idx, date_x_room_id in enumerate(solution):
        event = lessons[event_idx]
        schedule = date_x_room[date_x_room_id]
        date = schedule["date"]

        if employee in event["employees"]:
            if not inverted:
                if (date["day"], date["timeslot"]) in forbidden_slots:
                    return -1
            else:
                if (date["day"], date["timeslot"]) not in forbidden_slots:
                    return -1

    return 0

def evaluate_employee_subsequent_timeslots(constraint, solution, lessons, date_x_room):
    employee = constraint["owner"]
    limit = constraint["fields"]["limit"]
    # invert ignored
    # employee is not allowed to have more than limit lessons in a row

    employee = constraint["owner"]
    limit = constraint["fields"]["limit"]
    employee_schedule = {}

    for event_idx, date_x_room_id in enumerate(solution):
        event = lessons[event_idx]
        schedule = date_x_room[date_x_room_id]
        date = schedule["date"]

        if employee in event["employees"]:
            if date["day"] not in employee_schedule:
                employee_schedule[date["day"]] = []
            employee_schedule[date["day"]].append(date["timeslot"])

    violations = 0

    for day, timeslots in employee_schedule.items():
        sorted_slots = sorted(timeslots)
        consecutive_count = 1
        for i in range(1, len(sorted_slots)):
            if sorted_slots[i] == sorted_slots[i - 1] + 1:
                consecutive_count += 1
                if consecutive_count > limit:
                    violations += 1
            else:
                consecutive_count = 1

    return -violations

def evaluate_event_distribute_weekly_blocks(constraint, solution, lessons, date_x_room):
    # if not inverted, events with the same name must not be on the same day
    # if inverted, then events with the same name must be on the same day

    event_name = constraint["fields"]["event"]
    inverted = constraint["inverted"]
    event_days = set()

    for event_idx, date_x_room_id in enumerate(solution):
        event = lessons[event_idx]
        if event["name"] == event_name:
            schedule = date_x_room[date_x_room_id]
            date = schedule["date"]
            if date["day"] in event_days:
                if not inverted:
                    return -1
            else:
                event_days.add(date["day"])

    if not inverted:
        return 0
    else:
        return 0 if len(event_days) <= 1 else -1
