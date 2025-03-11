def has_employee(employee, event):
    """Prüft, ob der Mitarbeiter im Event beteiligt ist."""
    return employee in event.get("employees", [])


def has_participant(participant, event):
    """Prüft, ob der Mitarbeiter im Event beteiligt ist."""
    return participant in event.get("participants", [])


def on_day(event, day):
    """Prüft, ob das Event an einem bestimmten Tag stattfindet."""
    return event.get("day") == day


def on_timeslot(event, timeslot):
    """Prüft, ob das Event im angegebenen Timeslot stattfindet."""
    return event.get("timeslot") == timeslot


def day(event):
    return event.get("day")


def timeslot(event):
    return event.get("timeslot")


def event_named(event, name):
    """Prüft, ob das Event den angegebenen Namen hat."""
    return event.get("name") == name


def events_by_name(events, name):
    return [event for event in events if event.get("name") == name]


def event_room_name(event):
    return event.get("room_name")


def events_by_employee(events, employee):
    return [event for event in events if employee in event.get("employees")]


def events_all_same_day(events, name):
    events = events_by_name(events, name)
    days = set()
    for event in events:
        if event["day"] not in days:
            days.add(event["day"])

    return len(days) == 1


def evaluate_expression(expression, solution, lessons, date_x_room):
    """
    Wertet einen DSL-Ausdruck aus und liefert das Ergebnis zurück.

    Dabei wird ein vereinfachter Kontext erstellt, in dem alle Events
    als Dictionary mit den Schlüsseln 'day', 'timeslot', 'employees' und 'name'
    verfügbar sind. Zudem stehen Hilfsfunktionen zur Verfügung, die das
    Schreiben von Constraints erleichtern.
    """

    # Kombiniere die Daten zu einer Liste von Events
    events = []
    for i, schedule_id in enumerate(solution):
        event = lessons[i]
        schedule = date_x_room[schedule_id]
        date = schedule["date"]
        room = schedule["date"]

        events.append({
            "name": event.get("name", None),
            "employees": event.get("employees", []),
            "participants": event.get("participants", []),
            "size": event.get("size"),
            "day": date.get("day"),
            "timeslot": date.get("timeslot"),
            "room_name": room.get("name"),
            "room_capacity": room.get("capacity"),
            "room_size": room.get("size"),
        })

    # Sichere Umgebung: nur erlaubte Funktionen und Daten
    safe_globals = {"__builtins__": None}
    safe_globals.update({
        "events": events,
        "has_employee": has_employee,
        "has_participant": has_participant,
        "on_day": on_day,
        "on_timeslot": on_timeslot,
        "day": day,
        "timeslot": timeslot,
        "event_room_name": event_room_name,
        "event_named": event_named,
        "events_by_name": events_by_name,
        "events_by_employee": events_by_employee,
        "events_all_same_day": events_all_same_day,
        "any": any,
        "all": all,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        "range": range,
    })

    try:
        result = eval(expression, safe_globals)
        if result:
            return 0
        else:
            return -1
    except Exception as e:
        print("Fehler beim Auswerten des Ausdrucks:", e)
        return -1
