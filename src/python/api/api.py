data = {}


def inject(new_data):
    global data
    data = new_data


def get_days_by_id():
    return list(range(1, data["metadata"]["days"] + 1))


def get_time_slots_by_id():
    """Returns a dictionary of time slot indices to time slot details."""
    return list(range(1, data["metadata"]["timeslots"] + 1))


def get_dates_by_id() -> dict[int, dict]:
    """Returns a dictionary of date indices to day and time slot details."""
    days_by_abbr = get_days_by_id()
    time_slots_by_id = get_time_slots_by_id()

    dates = {}
    index = 1
    for day in days_by_abbr:
        for timeslot in time_slots_by_id:
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

def get_constraints_hard():
    return data["constraints"]["hard"]

def get_constraints_soft():
    return data["constraints"]["soft"]
