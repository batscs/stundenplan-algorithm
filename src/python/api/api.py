data = {}


def inject(new_data):
    global data
    data = new_data


def get_days_by_id() -> dict[str, dict]:
    """Returns a dictionary of day abbreviations to day details."""
    return {day['Abbreviation']: day for day in data['Day']}


def get_time_slots_by_id() -> dict[int, dict]:
    """Returns a dictionary of time slot indices to time slot details."""
    return {idx + 1: ts for idx, ts in enumerate(data['TimeSlot'])}


def get_dates_by_id() -> dict[int, dict]:
    """Returns a dictionary of date indices to day and time slot details."""
    days_by_abbr = get_days_by_id()
    time_slots_by_id = get_time_slots_by_id()

    dates = {}
    index = 1
    for day_abbr, day in days_by_abbr.items():
        for ts_id, ts in time_slots_by_id.items():
            dates[index] = {
                'Day': day,
                'TimeSlot': ts
            }
            index += 1
    return dates


def get_priorities_by_id() -> dict[int, int]:
    """Returns a dictionary of priority ids to priority values."""
    return {idx + 1: p['Value'] for idx, p in enumerate(data['Priority'])}


def get_employee_types_by_id() -> dict[str, dict]:
    """Returns a dictionary of employee type names to details."""
    return {et['Name']: et for et in data['EmployeeType']}


def get_employees_by_id() -> dict[str, dict]:
    """Returns a dictionary of employee abbreviations to employee details."""
    employee_types = get_employee_types_by_id()

    employees = {}
    for emp in data['Employee']:
        emp_type = employee_types.get(emp['Employee Type'])
        employees[emp['Abbreviation']] = {**emp, 'EmployeeType': emp_type}
    return employees


def get_employee_dislikes_date() -> dict[tuple[str, int], int]:
    """Returns a mapping of (employee abbreviation, date index) to priority value."""
    dates_by_id = get_dates_by_id()
    priorities_by_id = get_priorities_by_id()

    dislikes = {}
    for ed in data['EmployeeDislikesDate']:
        employee = ed['Employee Abbreviation']
        day_abbr = ed['Day Abbreviation']
        time_slot_ids = map(int, ed['Time Slot Ids'].split(';'))
        priority = priorities_by_id.get(ed['Priority Value'])
        for ts_id in time_slot_ids:
            for date_id, date in dates_by_id.items():
                if date['Day']['Abbreviation'] == day_abbr and date['TimeSlot'] == ts_id:
                    dislikes[(employee, date_id)] = priority
    return dislikes


def get_rooms_by_id() -> dict[str, dict]:
    """Returns a dictionary of room abbreviations to room details."""

    rooms = {}
    for room in data['Room']:
        rooms[room['Abbreviation']] = {
            **room
        }
    return rooms


def get_terms_by_id() -> dict[str, dict]:
    """Returns a dictionary of term names to details."""
    return {term['Name']: term for term in data['Term']}


def get_courses_by_id() -> dict[str, dict]:
    """Returns a dictionary of course abbreviations to course details."""
    return {course['Abbreviation']: course for course in data['Course']}


def get_semesters_by_id() -> dict[int, dict]:
    """Returns a dictionary of semester values to details."""
    return {s['Value']: s for s in data['Semester']}


def get_events_by_id() -> dict[str, dict]:
    """Returns a dictionary of event names to event details."""

    events = {}
    for event in data['Event']:
        participants = {}
        if 'Participants' in event:
            for participant in event['Participants'].split(';'):
                course, semesters = participant.split(':')
                participants[course] = list(map(int, semesters.split(',')))
        disallowed_days = event['Disallowed Days'].split(';')

        events[event['Name']] = {
            **event,
            'Participants': participants,
            'RoomType': event['Room Type'],
            'DisallowedDays': disallowed_days
        }
    return events

def get_constraints_hard():
    # TODO noch nicht in JSON Input
    return []

def get_constraints_soft():
    # TODO noch nicht in JSON Input
    return []