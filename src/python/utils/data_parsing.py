import inspect
from pandas import DataFrame
from src.python.db.dao.day_dao import DayDAO
from src.python.db.dao.time_slot_dao import TimeSlotDAO
from src.python.db.dao.employee_type_dao import EmployeeTypeDAO
from src.python.db.dao.employee_dao import EmployeeDAO
from src.python.db.dao.participant_size_dao import ParticipantSizeDAO
from src.python.db.dao.room_type_dao import RoomTypeDAO
from src.python.db.dao.room_dao import RoomDAO
from src.python.db.dao.course_dao import CourseDAO
from src.python.db.dao.term_dao import TermDAO
from src.python.db.dao.semester_dao import SemesterDAO
from src.python.db.dao.event_dao import EventDAO
from src.python.db.dao.employee_holds_event import EmployeeHoldsEventDAO
from src.python.db.dao.course_contains_event_dao import CourseContainsEventDAO
from src.python.db.dao.priority_dao import PriorityDAO
from src.python.db.dao.date_dao import DateDAO
from src.python.db.dao.employee_dislikes_date_dao import EmployeeDislikesDateDAO
from src.python.db.dao.event_disallows_day_dao import EventDisallowsDayDAO
from src.python.db.dto.day_dto import DayDTO
from src.python.db.dto.time_slot_dto import TimeSlotDTO
from src.python.db.dto.employee_type_dto import EmployeeTypeDTO
from src.python.db.dto.employee_dto import EmployeeDTO
from src.python.db.dto.participant_size import ParticipantSizeDTO
from src.python.db.dto.room_type_dto import RoomTypeDTO
from src.python.db.dto.room_dto import RoomDTO
from src.python.db.dto.course_dto import CourseDTO
from src.python.db.dto.term_dto import TermDTO
from src.python.db.dto.semester_dto import SemesterDTO
from src.python.db.dto.event_dto import EventDTO
from src.python.db.dto.employee_holds_event_dto import EmployeeHoldsEventDTO
from src.python.db.dto.course_contains_event_dto import CourseContainsEventDTO
from src.python.db.dto.priority_dto import PriorityDTO
from src.python.db.dto.date_dto import DateDTO
from src.python.db.dto.employee_dislikes_date_dto import EmployeeDislikesDateDTO
from src.python.db.dto.event_disallows_day_dto import EventDisallowsDayDTO
from src.python.log.logger import logger_app


def parse_days(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the days from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the days to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the days in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    day_dtos: list[DayDTO] = [
        DayDTO(id=0, abbreviation=row["Abbreviation"], name=row["Name"])
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        DayDAO().insert_all(day_dtos)
    else:
        for day_dto in day_dtos:
            DayDAO().insert(day_dto)


def parse_time_slots(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the time slots from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the time slots to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the time slots in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    time_slot_dtos: list[TimeSlotDTO] = [
        TimeSlotDTO(id=0, start_time=row["Start Time"], end_time=row["End Time"])
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        TimeSlotDAO().insert_all(time_slot_dtos)
    else:
        for time_slot_dto in time_slot_dtos:
            TimeSlotDAO().insert(time_slot_dto)


def insert_dates(fast_and_least_verbose: bool) -> None:
    """Inserts date entities for all combinations of days and time slots in the database.

    Args:
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the dates in the database.
    """

    # Cached for efficiency.
    time_slot_dtos: list[TimeSlotDTO] = TimeSlotDAO().select_all()
    date_dtos: list[DateDTO] = [
        DateDTO(id=0, day_id=day_dto.id, time_slot_id=time_slot_dto.id)
        for day_dto in DayDAO().select_all()
        for time_slot_dto in time_slot_dtos
    ]
    if fast_and_least_verbose:
        DateDAO().insert_all(date_dtos)
    else:
        for date_dto in date_dtos:
            DateDAO().insert(date_dto)


def parse_employee_types(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the employee types from the excel file and inserts corresponding entities in the
    database.

    Args:
        data_frame: Data frame containing the employee types to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the employee types in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    employee_type_dtos: list[EmployeeTypeDTO] = [
        EmployeeTypeDTO(id=0, name=row["Name"])
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        EmployeeTypeDAO().insert_all(employee_type_dtos)
    else:
        for employee_type_dto in employee_type_dtos:
            EmployeeTypeDAO().insert(employee_type_dto)


def parse_employees(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the employees from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the employees to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the employees in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    employee_types_by_name: dict[str, EmployeeTypeDTO] = {
        employee_type_dto.name: employee_type_dto
        for employee_type_dto in EmployeeTypeDAO().select_all()
    }
    employee_dtos: list[EmployeeDTO] = [
        EmployeeDTO(
            id=0,
            abbreviation=row["Abbreviation"],
            title=row["Title"],
            first_name=row["First Name"],
            last_name=row["Last Name"],
            employee_type_id=employee_types_by_name[row["Employee Type"]].id,
        )
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        EmployeeDAO().insert_all(employee_dtos)
    else:
        for employee_dto in employee_dtos:
            EmployeeDAO().insert(employee_dto)


def parse_participant_sizes(
    data_frame: DataFrame, fast_and_least_verbose: bool
) -> None:
    """Parses the participant sizes from the excel file and inserts corresponding entities in the
    database.

    Args:
        data_frame: Data frame containing the participant sizes to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the participant sizes in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    participant_size_dtos: list[ParticipantSizeDTO] = [
        ParticipantSizeDTO(id=0, name=row["Name"], ordinal=row["Ordinal"])
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        ParticipantSizeDAO().insert_all(participant_size_dtos)
    else:
        for participant_size_dto in participant_size_dtos:
            ParticipantSizeDAO().insert(participant_size_dto)


def parse_room_types(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the room types from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the room types to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the room types in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    room_type_dtos: list[RoomTypeDTO] = [
        RoomTypeDTO(id=0, name=row["Name"])
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        RoomTypeDAO().insert_all(room_type_dtos)
    else:
        for room_type_dto in room_type_dtos:
            RoomTypeDAO().insert(room_type_dto)


def parse_rooms(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the rooms from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the rooms to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the rooms in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    participant_sizes_by_name: dict[str, ParticipantSizeDTO] = {
        participant_size_dto.name: participant_size_dto
        for participant_size_dto in ParticipantSizeDAO().select_all()
    }
    room_types_by_name: dict[str, RoomTypeDTO] = {
        room_type_dto.name: room_type_dto
        for room_type_dto in RoomTypeDAO().select_all()
    }
    room_dtos: list[RoomDTO] = [
        RoomDTO(
            id=0,
            abbreviation=row["Abbreviation"],
            name=row["Name"],
            participant_size_id=participant_sizes_by_name[row["Capacity"]].id,
            room_type_id=room_types_by_name[row["Room Type"]].id,
        )
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        RoomDAO().insert_all(room_dtos)
    else:
        for room_dto in room_dtos:
            RoomDAO().insert(room_dto)


def parse_courses(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the courses from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the courses to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the courses in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    course_dtos: list[CourseDTO] = [
        CourseDTO(id=0, abbreviation=row["Abbreviation"], name=row["Name"])
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        CourseDAO().insert_all(course_dtos)
    else:
        for course_dto in course_dtos:
            CourseDAO().insert(course_dto)


def parse_terms(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the terms from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the terms to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the terms in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    term_dtos: list[TermDTO] = [
        TermDTO(id=0, name=row["Name"]) for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        TermDAO().insert_all(term_dtos)
    else:
        for term_dto in term_dtos:
            TermDAO().insert(term_dto)


def parse_semesters(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the semesters from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the semesters to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the semesters in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    semester_dtos: list[SemesterDTO] = [
        SemesterDTO(id=0, value=row["Value"])
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        SemesterDAO().insert_all(semester_dtos)
    else:
        for semester_dto in semester_dtos:
            SemesterDAO().insert(semester_dto)


def parse_events(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the events from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the events to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the events in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    courses_by_abbreviation: dict[str, CourseDTO] = {
        course_dto.abbreviation: course_dto for course_dto in CourseDAO().select_all()
    }
    terms_by_name: dict[str, TermDTO] = {
        term_dto.name: term_dto for term_dto in TermDAO().select_all()
    }
    participant_sizes_by_name: dict[str, ParticipantSizeDTO] = {
        participant_size_dto.name: participant_size_dto
        for participant_size_dto in ParticipantSizeDAO().select_all()
    }
    room_types_by_name: dict[str, RoomTypeDTO] = {
        room_type_dto.name: room_type_dto
        for room_type_dto in RoomTypeDAO().select_all()
    }
    employees_by_abbreviation: dict[str, EmployeeDTO] = {
        employee_dto.abbreviation: employee_dto
        for employee_dto in EmployeeDAO().select_all()
    }
    semesters_by_value: dict[int, SemesterDTO] = {
        semester_dto.value: semester_dto for semester_dto in SemesterDAO().select_all()
    }
    days_by_abbreviation: dict[str, DayDTO] = {
        day_dto.abbreviation: day_dto for day_dto in DayDAO().select_all()
    }
    event_dtos: list[EventDTO] = []
    employee_holds_event_dtos: list[EmployeeHoldsEventDTO] = []
    course_contains_event_dtos: list[CourseContainsEventDTO] = []
    event_disallows_day_dtos: list[EventDisallowsDayDTO] = []
    for index, row in enumerate(data_frame.to_dict(orient="records")):
        # Caution: This assumes that sqlite uses autoincremented ids starting from 1.
        event_id: int = index + 1
        event_dtos.append(
            EventDTO(
                id=0,
                name=row["Name"],
                weekly_blocks=int(row["Weekly Blocks"]),
                term_id=terms_by_name[row["Term"]].id,
                participant_size_id=participant_sizes_by_name[
                    row["Participant Size"]
                ].id,
                room_type_id=room_types_by_name[row["Room Type"]].id,
            )
        )
        # Events are allowed to have no employees. A common example are course projects that
        # can't really be assigned to a specific employee.
        if row["Employees"]:
            for employee_abbreviation in row["Employees"].split(","):
                employee_holds_event_dtos.append(
                    EmployeeHoldsEventDTO(
                        employee_id=employees_by_abbreviation[employee_abbreviation].id,
                        event_id=event_id,
                    )
                )
        participants: dict[str, list[int]] = {}
        # Events are allowed to have no mandatory participants. A common example are seminars,
        # for which the students of different courses decide if they'd like to participate.
        if row["Participants"]:
            for participant in row["Participants"].split(";"):
                # TODO if clause could be removed if it is assured that participants key ALWAYS exists
                if participant != "nan":
                    course_abbreviation, semesters = participant.split(":")
                    participants[course_abbreviation] = [
                        int(semester) for semester in semesters.split(",")
                    ]

            for course_abbreviation, semesters in participants.items():
                for semester in semesters:
                    course_contains_event_dtos.append(
                        CourseContainsEventDTO(
                            course_id=courses_by_abbreviation[course_abbreviation].id,
                            semester_id=semesters_by_value[semester].id,
                            event_id=event_id,
                        )
                    )
        for day_abbreviation in row["Disallowed Days"].split(";"):
            event_disallows_day_dtos.append(
                EventDisallowsDayDTO(
                    event_id=event_id, day_id=days_by_abbreviation[day_abbreviation].id
                )
            )
    if fast_and_least_verbose:
        EventDAO().insert_all(event_dtos)
        EmployeeHoldsEventDAO().insert_all(employee_holds_event_dtos)
        CourseContainsEventDAO().insert_all(course_contains_event_dtos)
        EventDisallowsDayDAO().insert_all(event_disallows_day_dtos)
    else:
        for event_dto in event_dtos:
            EventDAO().insert(event_dto)
        for employee_holds_event_dto in employee_holds_event_dtos:
            EmployeeHoldsEventDAO().insert(employee_holds_event_dto)
        for course_contains_event_dto in course_contains_event_dtos:
            CourseContainsEventDAO().insert(course_contains_event_dto)
        for event_disallows_day_dto in event_disallows_day_dtos:
            EventDisallowsDayDAO().insert(event_disallows_day_dto)


def parse_priorities(data_frame: DataFrame, fast_and_least_verbose: bool) -> None:
    """Parses the priorities from the excel file and inserts corresponding entities in the database.

    Args:
        data_frame: Data frame containing the priorities to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the priorities in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    priority_dtos: list[PriorityDTO] = [
        PriorityDTO(id=0, value=row["Value"])
        for row in data_frame.to_dict(orient="records")
    ]
    if fast_and_least_verbose:
        PriorityDAO().insert_all(priority_dtos)
    else:
        for priority_dto in priority_dtos:
            PriorityDAO().insert(priority_dto)


def parse_employee_dislikes_date(
    data_frame: DataFrame, fast_and_least_verbose: bool
) -> None:
    """Parses the dates disliked by certain employees from the excel file and inserts corresponding
    entities in the database.

    Args:
        data_frame: Data frame containing the disliked dates to parse.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way.

    Raises:
        `sqlite3.Error`: If any error occurs while inserting the disliked dates in the database.
    """
    logger_app.debug(f"{inspect.currentframe().f_code.co_name} count: {len(data_frame.index)}")

    employees_by_abbreviation: dict[str, EmployeeDTO] = {
        employee_dto.abbreviation: employee_dto
        for employee_dto in EmployeeDAO().select_all()
    }
    days_by_abbreviation: dict[str, DayDTO] = {
        day_dto.abbreviation: day_dto for day_dto in DayDAO().select_all()
    }
    priorities_by_value: dict[int, PriorityDTO] = {
        priority_dto.value: priority_dto for priority_dto in PriorityDAO().select_all()
    }
    dates_by_day_and_time_slot_ids: dict[tuple[int, int], DateDTO] = {
        (date_dto.day_id, date_dto.time_slot_id): date_dto
        for date_dto in DateDAO().select_all()
    }
    employee_dislikes_date_dtos: list[EmployeeDislikesDateDTO] = []
    for row in data_frame.to_dict(orient="records"):
        employee_id: int = employees_by_abbreviation[row["Employee Abbreviation"]].id
        day_id: int = days_by_abbreviation[row["Day Abbreviation"]].id
        priority_id: int = priorities_by_value[row["Priority Value"]].id
        for time_slot_id in row["Time Slot Ids"].split(";"):
            employee_dislikes_date_dtos.append(
                EmployeeDislikesDateDTO(
                    employee_id=employee_id,
                    date_id=dates_by_day_and_time_slot_ids[
                        (day_id, int(time_slot_id))
                    ].id,
                    priority_id=priority_id,
                )
            )
    if fast_and_least_verbose:
        EmployeeDislikesDateDAO().insert_all(employee_dislikes_date_dtos)
    else:
        for employee_dislikes_date_dto in employee_dislikes_date_dtos:
            EmployeeDislikesDateDAO().insert(employee_dislikes_date_dto)