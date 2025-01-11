from api.models.day import Day
from api.models.time_slot import TimeSlot
from api.models.date import Date
from api.models.term import Term
from api.models.participant_size import ParticipantSize
from api.models.room_type import RoomType
from api.models.room import Room
from api.models.priority import Priority
from api.models.employee_type import EmployeeType
from api.models.employee import Employee
from api.models.course import Course
from api.models.semester import Semester
from api.models.event import Event
from db.dao.day_dao import DayDAO
from db.dao.time_slot_dao import TimeSlotDAO
from db.dao.date_dao import DateDAO
from db.dao.participant_size_dao import ParticipantSizeDAO
from db.dao.room_type_dao import RoomTypeDAO
from db.dao.room_dao import RoomDAO
from db.dao.priority_dao import PriorityDAO
from db.dao.employee_type_dao import EmployeeTypeDAO
from db.dao.employee_dao import EmployeeDAO
from db.dao.course_dao import CourseDAO
from db.dao.semester_dao import SemesterDAO
from db.dao.employee_holds_event import EmployeeHoldsEventDAO
from db.dao.course_contains_event_dao import CourseContainsEventDAO
from db.dao.event_dao import EventDAO
from db.dao.employee_dislikes_date_dao import EmployeeDislikesDateDAO
from db.dao.term_dao import TermDAO
from db.dao.event_disallows_day_dao import EventDisallowsDayDAO
from db.dto.employee_holds_event_dto import EmployeeHoldsEventDTO
from db.dto.course_contains_event_dto import CourseContainsEventDTO
from db.dto.event_disallows_day_dto import EventDisallowsDayDTO


def get_days_by_id() -> dict[int, Day]:
    """Returns a dictionary of day ids to days.

    Returns:
        A dictionary of day ids to days.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the days.
    """
    return {
        day_dto.id: Day(abbreviation=day_dto.abbreviation, name=day_dto.name)
        for day_dto in DayDAO().select_all()
    }


def get_time_slots_by_id() -> dict[int, TimeSlot]:
    """Returns a dictionary of time slot ids to time slots.

    Returns:
        A dictionary of time slot ids to time slot.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the time slots.
    """
    return {
        time_slot_dto.id: TimeSlot(
            start_time=time_slot_dto.start_time, end_time=time_slot_dto.end_time
        )
        for time_slot_dto in TimeSlotDAO().select_all()
    }


def get_dates_by_id() -> dict[int, Date]:
    """Returns a dictionary of date ids to dates.

    Returns:
        A dictionary of date ids to dates.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the dates.
    """
    days_by_id: dict[int, Day] = get_days_by_id()
    time_slots_by_id: dict[int, TimeSlot] = get_time_slots_by_id()
    return {
        date_dto.id: Date(
            day=days_by_id[date_dto.day_id],
            time_slot=time_slots_by_id[date_dto.time_slot_id],
        )
        for date_dto in DateDAO().select_all()
    }


def get_priorities_by_id() -> dict[int, Priority]:
    """Returns a dictionary of priority ids to priorities.

    Returns:
        A dictionary of priority ids to priorities.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the priorities.
    """
    return {
        priority_dto.id: Priority(value=priority_dto.value)
        for priority_dto in PriorityDAO().select_all()
    }


def get_employee_types_by_id() -> dict[int, EmployeeType]:
    """Returns a dictionary of employee type ids to employee types.

    Returns:
        A dictionary of employee type ids to employee types.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the employee types.
    """
    return {
        employee_type_dto.id: EmployeeType(name=employee_type_dto.name)
        for employee_type_dto in EmployeeTypeDAO().select_all()
    }


def get_employees_by_id() -> dict[int, Employee]:
    """Returns a dictionary of employee ids to employees.

    Returns:
        A dictionary of employee ids to employees.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the employees.
    """
    employee_types_by_id: dict[int, EmployeeType] = get_employee_types_by_id()
    return {
        employee_dto.id: Employee(
            abbreviation=employee_dto.abbreviation,
            title=employee_dto.title,
            first_name=employee_dto.first_name,
            last_name=employee_dto.last_name,
            employee_type=employee_types_by_id[employee_dto.employee_type_id],
        )
        for employee_dto in EmployeeDAO().select_all()
    }


def get_employee_dislikes_date() -> dict[tuple[int, int], int]:
    """Returns a dictionary that maps tuples of employee ids and date ids to priority ids.

    Returns:
        A dictionary mapping tuples of employee ids and date ids to priority ids.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the dates disliked by the employees.
    """
    return {
        (
            employee_dislikes_date_dto.employee_id,
            employee_dislikes_date_dto.date_id,
        ): employee_dislikes_date_dto.priority_id
        for employee_dislikes_date_dto in EmployeeDislikesDateDAO().select_all()
    }


def get_participant_sizes_by_id() -> dict[int, ParticipantSize]:
    """Returns a dictionary of participant size ids to participant sizes.

    Returns:
        A dictionary of participant size ids to participant sizes.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the participant sizes.
    """
    return {
        participant_size_dto.id: ParticipantSize(
            name=participant_size_dto.name, ordinal=participant_size_dto.ordinal
        )
        for participant_size_dto in ParticipantSizeDAO().select_all()
    }


def get_room_types_by_id() -> dict[int, RoomType]:
    """Returns a dictionary of room type ids to room types.

    Returns:
        A dictionary of room type ids to room types.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the room types.
    """
    return {
        room_type_dto.id: RoomType(name=room_type_dto.name)
        for room_type_dto in RoomTypeDAO().select_all()
    }


def get_rooms_by_id() -> dict[int, Room]:
    """Returns a dictionary of room ids to rooms.

    Returns:
        A dictionary of room ids to rooms.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the rooms.
    """
    participant_sizes_by_id: dict[int, ParticipantSize] = get_participant_sizes_by_id()
    room_types_by_id: dict[int, RoomType] = get_room_types_by_id()
    return {
        room_dto.id: Room(
            abbreviation=room_dto.abbreviation,
            name=room_dto.name,
            participant_size=participant_sizes_by_id[room_dto.participant_size_id],
            room_type=room_types_by_id[room_dto.room_type_id],
        )
        for room_dto in RoomDAO().select_all()
    }


def get_terms_by_id() -> dict[int, Term]:
    """Returns a dictionary of term ids to terms.

    Returns:
        A dictionary of term ids to terms.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the terms.
    """
    return {
        term_dto.id: Term(name=term_dto.name) for term_dto in TermDAO().select_all()
    }


def get_courses_by_id() -> dict[int, Course]:
    """Returns a dictionary of course ids to courses.

    Returns:
        A dictionary of course ids to courses.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the courses.
    """
    return {
        course_dto.id: Course(
            abbreviation=course_dto.abbreviation, name=course_dto.name
        )
        for course_dto in CourseDAO().select_all()
    }


def get_semesters_by_id() -> dict[int, Semester]:
    """Returns a dictionary of semester ids to semesters.

    Returns:
        A dictionary of semester ids to semesters.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the semesters.
    """
    return {
        semester_dto.id: Semester(value=semester_dto.value)
        for semester_dto in SemesterDAO().select_all()
    }


def get_events_by_id() -> dict[int, Event]:
    """Returns a dictionary of event ids to events.

    Returns:
        A dictionary of event ids to events.

    Raises:
        `sqlite3.Error`: If any error occurs while getting the events.
    """
    employee_holds_event_dtos: list[EmployeeHoldsEventDTO] = (
        EmployeeHoldsEventDAO().select_all()
    )
    course_contains_event_dtos: list[CourseContainsEventDTO] = (
        CourseContainsEventDAO().select_all()
    )
    event_disallows_day_dtos: list[EventDisallowsDayDTO] = (
        EventDisallowsDayDAO().select_all()
    )
    terms_by_id: dict[int, Term] = get_terms_by_id()
    participant_sizes_by_id: dict[int, ParticipantSize] = get_participant_sizes_by_id()
    room_types_by_id: dict[int, RoomType] = get_room_types_by_id()
    events_by_id: dict[int, Event] = {}
    days_by_id: dict[int, Day] = get_days_by_id()
    for event_dto in EventDAO().select_all():
        employee_ids: list[int] = [
            employee_holds_event_dto.employee_id
            for employee_holds_event_dto in employee_holds_event_dtos
            if employee_holds_event_dto.event_id == event_dto.id
        ]
        participants: dict[int, list[int]] = {}
        for course_contains_event_dto in course_contains_event_dtos:
            if course_contains_event_dto.event_id == event_dto.id:
                if not course_contains_event_dto.course_id in participants:
                    participants[course_contains_event_dto.course_id] = []
                participants[course_contains_event_dto.course_id].append(
                    course_contains_event_dto.semester_id
                )
        disallowed_days: list[Day] = []
        for event_disallows_day_dto in event_disallows_day_dtos:
            if event_disallows_day_dto.event_id == event_dto.id:
                disallowed_days.append(days_by_id[event_disallows_day_dto.day_id])
        events_by_id[event_dto.id] = Event(
            name=event_dto.name,
            employee_ids=employee_ids,
            participants=participants,
            weekly_blocks=event_dto.weekly_blocks,
            term=terms_by_id[event_dto.term_id],
            participant_size=participant_sizes_by_id[event_dto.participant_size_id],
            room_type=room_types_by_id[event_dto.room_type_id],
            disallowed_days=disallowed_days,
        )
    return events_by_id
