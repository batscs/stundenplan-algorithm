import json
import os
import sys
import pytz
from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime
from io import StringIO
from tabulate import tabulate
from typing import Any

import excel_parser
from api.api import get_time_slots_by_id
from api.models import day
from db.database import Database
from genetic_algorithm import NUM_GENERATIONS, genetic_algorithm
from utils import path_utils, time_utils
from log import logging_config


def parse_arguments() -> tuple[int, str, str, bool]:
    """Parses command-line arguments for the genetic algorithm scheduling program.

    This function sets up the argument parser with the following options:
    - Generations: Specifies how many generations the genetic algorithm will run (default is 20000).
    - Term: Determines whether the term is summer or winter (default is summer).
    - Output format: Chooses the format for printing the results (default is tabular text format).

    If any error occurs while parsing, the help message is printed to stderr and the program exits
    using an appropriate exit code.

    Returns:
        A tuple containing the following parsed arguments:
        generations: Bumber of generations for the genetic algorithm.
        term: Term to be used for the scheduling ("Sommer" or "Winter").
        output_format: Output format type ("Tabular").
    """
    parser: ArgumentParser = ArgumentParser(
        prog="fhw_timeschedule_generator",
        description="This program uses a genetic algorithm to optimize the scheduling of events "
        + "for a given term. It processes input parameters for the number of generations, "
        + "term (summer or winter), and the output format of the results.",
    )
    parser.add_argument(
        "-g",
        "--generations",
        metavar="N",
        type=int,
        default=NUM_GENERATIONS,
        help=f"Set number of generations (defaults to {NUM_GENERATIONS})",
    )
    parser.add_argument(
        "-s",
        "--summer",
        action="store_true",
        help="Set summer term (default)",
        default=True,
    )
    parser.add_argument(
        "-w",
        "--winter",
        action="store_true",
        help="Set winter term (overrides -s)",
        default=False,
    )
    parser.add_argument(
        "-t",
        "--print-tabular",
        action="store_true",
        help="Print result to a .txt file using a table format (default)",
        default=True,
    )
    parser.add_argument(
        "-d",
        "--debug_mode",
        action="store_true",
        help="Turn debug mode on",
        default=False,
    )
    # parser.add_argument(
    #     "-x",
    #     "--print-xml",
    #     action="store_true",
    #     help="Print result to an .xml file using the splan format.",
    #     default=False,
    # )
    try:
        args = parser.parse_args()
        return (
            args.generations,
            "Winter" if args.winter else "Sommer",
            # TODO: Use when print to xml is implemented: "XML" if args.print_xml else "Tabular"
            "Tabular",
            args.debug_mode,
        )
    except SystemExit as e:
        if e.code != 0:
            print(parser.format_help(), file=sys.stderr)
        exit(e.code)


def save_tabular(
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
        with open(
            os.path.join(solution_directory, solution_filename), "w", encoding="UTF8"
        ) as solution_file:
            solution_file.write(f"Fitness: {fitness}\n{cli_print}")
        if debug:
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


def main() -> None:
    generations, term, output_format, debug_mode = parse_arguments()
    logging_config.configure_logging()
    Database().initialize(delete_database_file=True)
    excel_parser.parse()
    runtime, _, _, _ = genetic_algorithm(1, term)
    estimated_runtime: float = generations * runtime
    print(f"Genetic algorithm started (generations = {generations}, term = {term})")
    print(
        f"Estimated runtime up to: {time_utils.seconds_to_formatted_duration(estimated_runtime)}"
    )
    runtime, parsed_solution, fitness, generations_completed = genetic_algorithm(
        generations, term
    )
    print(f"\nSolution fitness: {fitness}")
    print(f"Generations completed: {generations_completed}")
    print(f"Actual runtime: {time_utils.seconds_to_formatted_duration(runtime)}")
    save_tabular(parsed_solution, fitness, debug_mode)
    exit(0)


if __name__ == "__main__":
    main()
