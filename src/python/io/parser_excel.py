import os
import pandas
from pandas import DataFrame

from src.python.db.database import Database
from src.python.log import logging_config
from src.python.utils import path_utils

from src.python.utils import data_parsing

EXCEL_FILE_NAME: str = "FHW.xlsm"
"""Name of the excel file to parse."""

DEFAULT_EXCEL_FILE_PATH: str = os.path.join(path_utils.RESOURCES_PATH, EXCEL_FILE_NAME)
"""Default path of the excel file containing the data to parse."""

def parse(
    excel_file_path: str = DEFAULT_EXCEL_FILE_PATH,
    fast_and_least_verbose: bool = True,
) -> None:
    """Parses an excel file into the database.

    Args:
        excel_file_path: Path to the excel file to parse the data from, by default the path of the
            standard excel file `DEFAULT_EXCEL_FILE_PATH`.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way,
            by default `True`.

    Raises:
        `FileNotFoundError`: If `excel_file_path` does not exist.
        `sqlite3.Error`: If any error occurs while interacting with the database.
    """

    data_frames: dict[str, DataFrame] = pandas.read_excel(
        excel_file_path, sheet_name=None
    )

    for data_frame in data_frames.values():
        data_frame.fillna("", inplace=True)

    data_parsing.parse_days(data_frames["Day"], fast_and_least_verbose)
    data_parsing.parse_time_slots(data_frames["TimeSlot"], fast_and_least_verbose)
    data_parsing.insert_dates(fast_and_least_verbose)
    data_parsing.parse_employee_types(data_frames["EmployeeType"], fast_and_least_verbose)
    data_parsing.parse_employees(data_frames["Employee"], fast_and_least_verbose)
    data_parsing.parse_participant_sizes(data_frames["ParticipantSize"], fast_and_least_verbose)
    data_parsing.parse_room_types(data_frames["RoomType"], fast_and_least_verbose)
    data_parsing.parse_rooms(data_frames["Room"], fast_and_least_verbose)
    data_parsing.parse_courses(data_frames["Course"], fast_and_least_verbose)
    data_parsing.parse_terms(data_frames["Term"], fast_and_least_verbose)
    data_parsing.parse_semesters(data_frames["Semester"], fast_and_least_verbose)
    data_parsing.parse_events(data_frames["Event"], fast_and_least_verbose)
    data_parsing.parse_priorities(data_frames["Priority"], fast_and_least_verbose)
    data_parsing.parse_employee_dislikes_date(
        data_frames["EmployeeDislikesDate"], fast_and_least_verbose
    )


def main() -> None:
    logging_config.configure_logging()
    Database().initialize(delete_database_file=True)
    parse()


if __name__ == "__main__":
    main()
