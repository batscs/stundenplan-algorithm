from src.python.log.logger import logger_app

data = {}


def inject(new_data):
    logger_app.debug("Loaded input data for Stundenplan creation")
    global data
    data = new_data


def get_schedule() -> [(int, int)]:
    """Returns a dictionary of date indices to day and time slot details."""
    return data["timeslots"]


def get_rooms() -> dict[str, dict]:
    """Returns a dictionary of room abbreviations to room details."""
    return data["rooms"]


def get_events():
    """Returns a dictionary of event names to event details."""
    return data["events"]


def get_lessons():
    lessons = [
        event
        for event in get_events()
        for _ in range(event["weekly_blocks"])
    ]

    return lessons


def get_constraints_hard():
    return data["constraints"]["hard"]


def get_constraints_soft():
    return data["constraints"]["soft"]


def get_date_x_room():
    date_x_room = [
        {"date": d, "room": r}
        for d in get_schedule()
        for r in get_rooms()
    ]

    return date_x_room
