import json
import os
from collections import OrderedDict
from datetime import datetime
from typing import Any

import numpy as np
import pytz

from src.python.utils import path_utils

def printer_save(
    parsed_solution: dict[str, Any], fitness: int, debug_mode: bool = False
) -> None:
    """Saves the parsed solution as a JSON file.

    Args:
        parsed_solution: Best solution parsed into a human-readable format.
        fitness: Fitness of the best solution.
        debug_mode: Whether to print the JSON for debugging purposes, `False` by default.
    """

    def sort_time_table(parsed_solution: dict[str, Any]) -> OrderedDict[str, Any]:
        """Sorts the time table (ascending order) parsed from a PyGad solution.

        Args:
            parsed_solution: Best solution parsed into a human-readable format.

        Returns:
            An ordered dictionary containing the sorted data of the time table.
        """
        result: OrderedDict[str, Any] = OrderedDict()
        days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        for day_name in days:
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

    def save_as_json(
        sorted_time_table: OrderedDict[str, Any],
        # separated_time_tables: OrderedDict[str, Any],
        fitness: int,
        debug: bool = False,
    ) -> None:
        """Saves the formatted JSON time table into a file.

        Args:
            sorted_time_table: Sorted time table.
            separated_time_tables: Sorted and separated time tables.
            fitness: Fitness value of the solution.
            debug: Whether to print the JSON for debugging purposes, `False` by default.
        """
        current_time: str = (
            datetime.now(pytz.utc)
            .astimezone(pytz.timezone("Europe/Berlin"))
            .strftime("%Y-%m-%d_%H-%M-%S")
        )
        solution_filename: str = f"parsed_solution_{current_time}.json"
        solution_directory: str = path_utils.RESOURCE_OUTPUT_PATH
        os.makedirs(solution_directory, exist_ok=True)

        solution_filepath: str = os.path.join(solution_directory, solution_filename)

        # Prepare the JSON structure
        json_data = {
            "fitness": fitness,
            "complete_time_table": sorted_time_table,
            "constraints": parsed_solution["constraints"]
        }

        def custom_encoder(obj):
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, (np.ndarray,)):
                return obj.tolist()
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        with open(solution_filepath, "w", encoding="UTF8") as solution_file:
            json.dump(json_data, solution_file, ensure_ascii=False, indent=4, default=custom_encoder)

        if debug:
            print(f"Saving file to: {os.path.abspath(solution_filepath)}")
            print(json.dumps(json_data, ensure_ascii=False, indent=4, default=custom_encoder))

    solution: dict[str, Any] = json.loads(
        json.dumps(parsed_solution, ensure_ascii=False).replace("'", '"')
    )
    sorted_time_table: OrderedDict[str, Any] = sort_time_table(solution)
    save_as_json(sorted_time_table, fitness, debug_mode)
