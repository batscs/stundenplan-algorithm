from src.python.log.logger import logger_app

data = {}


def inject(new_data):
    logger_app.debug("Loaded input data for Stundenplan creation")
    global data
    data = new_data

def get_dates_by_id() -> dict[int, dict]:
    """Returns a dictionary of date indices to day and time slot details."""
    days = list(range(1, data["metadata"]["days"] + 1))
    timeslots = list(range(1, data["metadata"]["timeslots"] + 1))

    dates = {}
    index = 1
    for day in days:
        for timeslot in timeslots:
            dates[index] = {
                'day': day,
                'timeslot': timeslot
            }
            index += 1
    return dates

def get_rooms_by_id() -> dict[str, dict]:
    """Returns a dictionary of room abbreviations to room details."""

    rooms = {}
    for room in data['rooms']:
        rooms[room['name']] = {
            **room
        }
    return rooms


def get_events_by_id():
    """Returns a dictionary of event names to event details."""
    return data["events"]

def get_lessons():
    lessons = [
        event
        for event in get_events_by_id()
        for _ in range(event["weekly_blocks"])
    ]

    return lessons

def get_constraints_hard():
    return data["constraints"]["hard"]

def get_constraints_soft():
    return data["constraints"]["soft"]

def get_date_x_room():
    date_x_room = [
        (d, r)
        for d in get_dates_by_id().items()
        for r in get_rooms_by_id().items()
    ]

    return date_x_room