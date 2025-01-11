import json
import os
from collections import OrderedDict
from datetime import datetime
from io import StringIO
from typing import Any

import pytz
from tabulate import tabulate

from src.python.api.api import get_time_slots_by_id
from src.python.api.models import day
from src.python.utils import path_utils


def printer_save(
    parsed_solution: dict[str, Any], fitness: int, debug_mode: bool = False
) -> None:
    """Saves the parsed solution in a tabular format. The solution is organized and printed in a
    structured text table.

    Args:
        parsed_solution: Best solution parsed into a human-readable format.
        fitness: Fitness of the best solution.
    """

    def sort_time_table(parsed_solution: dict[str, Any]) -> OrderedDict[str, Any]:
        """Sorts the time table (ascending order) parsed from a PyGad solution.

        Args:
            parsed_solution: Best solution parsed into a human-readable format.

        Returns:
            An ordered dictionary containing the sorted data of the time table.
        """
        # Use an OrderedDict to have the days in the correct order.
        result: OrderedDict[str, Any] = OrderedDict()
        for day_name in day.NAMES:
            if day_name in parsed_solution:
                sorted_timeslots: OrderedDict[str, Any] = OrderedDict(
                    sorted(parsed_solution[day_name].items())
                )
                for timeslot, events in sorted_timeslots.items():
                    sorted_events: OrderedDict[str, Any] = OrderedDict(
                        sorted(events.items())
                    )
                    sorted_timeslots[timeslot] = sorted_events
                result[day_name] = sorted_timeslots
        return result

    def separate_time_tables(
        sorted_time_table: OrderedDict[str, Any]
    ) -> OrderedDict[str, Any]:
        """Separates the general solution into separate time tables for each semester and course
        and sorts the time tables by semesters and courses (ascending order).

        Args:
            sorted_time_table: Sorted time table of the general solution containing all the
            information.

        Returns:
            An ordered dictionary containing the separated of the time tables for each semester and
            course.
        """
        separated_time_tables: OrderedDict[str, Any] = OrderedDict()
        for day, times in sorted_time_table.items():
            for time, lectures in times.items():
                for lecture, rooms in lectures.items():
                    for room, courses in rooms.items():
                        for course, semesters in courses.items():
                            for semester in semesters:
                                semester_str: str = str(semester)
                                if semester_str not in separated_time_tables:
                                    separated_time_tables[semester_str] = {}
                                if course not in separated_time_tables[semester_str]:
                                    separated_time_tables[semester_str][course] = {}
                                if (
                                    day
                                    not in separated_time_tables[semester_str][course]
                                ):
                                    separated_time_tables[semester_str][course][
                                        day
                                    ] = {}
                                if (
                                    time
                                    not in separated_time_tables[semester_str][course][
                                        day
                                    ]
                                ):
                                    separated_time_tables[semester_str][course][day][
                                        time
                                    ] = {}
                                if (
                                    lecture
                                    not in separated_time_tables[semester_str][course][
                                        day
                                    ][time]
                                ):
                                    separated_time_tables[semester_str][course][day][
                                        time
                                    ][lecture] = room
        separate_time_tables: OrderedDict[str, Any] = OrderedDict(
            sorted(separated_time_tables.items())
        )
        for semester in separate_time_tables:
            separate_time_tables[semester] = OrderedDict(
                sorted(separated_time_tables[semester].items())
            )
        return separate_time_tables

    def sorted_time_table_to_cli_print(
        sorted_time_table: OrderedDict[str, Any],
        separated_time_tables: bool = False,
    ) -> str:
        """Formats the sorted time table to a text table using tabulate.

        Args:
            sorted_time_table: Sorted time table to format as a text table.
            separated_time_tables: Whether the time table should be displayed separated into
                several smaller ones.

        Returns:
            A string containing the sorted time table in a text table formatted by tabulate.
        """
        correct_time_slot_order: list[str] = [
            f"{timeslot.start_time.strftime('%H:%M')} - {timeslot.end_time.strftime('%H:%M')}"
            for timeslot in get_time_slots_by_id().values()]
        table_data: list[list[str]] = []
        for time in correct_time_slot_order:
            row: list[str] = [time]
            for day_name in sorted_time_table:
                if time in sorted_time_table[day_name]:
                    tasks = sorted_time_table[day_name][time]
                    if separated_time_tables:
                        row.append(" | ".join([f"{k}: {v}" for k, v in tasks.items()]))
                    else:
                        row.append(
                            " | ".join(
                                [
                                    (
                                        f'{task}: {", ".join([f"{k}: {v}" for k, v in subtasks.items()])}'
                                        if isinstance(subtasks, dict)
                                        else f"{task}: {subtasks}"
                                    )
                                    for task, subtasks in tasks.items()
                                ]
                            )
                        )
                else:
                    row.append("")
            table_data.append(row)
        headers: list[str] = ["Uhrzeit"] + day.NAMES
        return tabulate(table_data, headers, tablefmt="grid")

    def all_time_tables_to_cli_print(
        sorted_time_table: OrderedDict[str, Any],
        separated_time_tables: OrderedDict[str, Any],
    ) -> str:
        """Formats the sorted time table and the separated time tables to a text table using
        tabulate.

        Args:
            sorted_time_table: Sorted time table to format as a text table.
            separated_time_tables: Sorted and separated time tables to format as text tables.

        Returns:
            A string containing the sorted time table and separated time tables in text tables
            formatted by tabulate.
        """
        # StringIO for more efficient accumulation of strings (instead of concatenation).
        cli_print: StringIO = StringIO()
        complete_time_table: str = sorted_time_table_to_cli_print(
            sorted_time_table, separated_time_tables=False
        )
        cli_print.write(f"\nComplete time table:\n{complete_time_table}\n")
        for semester in separated_time_tables:
            cli_print.write(f"\n{str(semester)}. Semester:\n")
            for course in separated_time_tables[semester]:
                separate_time_table: str = sorted_time_table_to_cli_print(
                    separated_time_tables[semester][course], separated_time_tables=True
                )
                cli_print.write(
                    f"\nCourse: {str(course)}\n{separate_time_table}\n\n"
                )
        return cli_print.getvalue()

    def save_cli_print(cli_print: str, debug: bool = False) -> None:
        """Saves the formatted text time table into a file.

        Args:
            cli_print: Text time table formatted using tabulate.
            debug: Whether to print `cli_print` for debugging purposes, `False` by default.
        """
        current_time: str = (
            datetime.now(pytz.utc)
            .astimezone(pytz.timezone("Europe/Berlin"))
            .strftime("%Y-%m-%d_%H-%M-%S")
        )
        solution_filename: str = f"parsed_solution_{current_time}.txt"
        solution_directory: str = os.path.join(path_utils.SRC_PATH, "..", "output")
        os.makedirs(solution_directory, exist_ok=True)

        # Combine directory and filename for the full path
        solution_filepath: str = os.path.join(solution_directory, solution_filename)

        with open(solution_filepath, "w", encoding="UTF8") as solution_file:
            solution_file.write(f"Fitness: {fitness}\n{cli_print}")

        if debug:
            # Print the correct absolute path
            print(f"Saving file to: {os.path.abspath(solution_filepath)}")
            print(f"Parsed solution:\n{cli_print}")

    solution: dict[str, Any] = json.loads(
        json.dumps(parsed_solution, ensure_ascii=False).replace("'", '"')
    )
    sorted_time_table: OrderedDict[str, Any] = sort_time_table(solution)
    separated_time_tables: OrderedDict[str, Any] = separate_time_tables(
        sorted_time_table
    )
    cli_print: str = all_time_tables_to_cli_print(
        sorted_time_table, separated_time_tables
    )
    save_cli_print(cli_print, debug_mode)