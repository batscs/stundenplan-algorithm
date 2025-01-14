import json
import os
from collections import OrderedDict
from datetime import datetime
from typing import Any

import numpy as np
import pytz

from src.python.utils import path_utils

def printer_save(
    parsed_solution: dict[str, Any]
) -> None:
    """Saves the parsed solution as a JSON file.

    Args:
        parsed_solution: Best solution parsed into a human-readable format.
        fitness: Fitness of the best solution.
        debug_mode: Whether to print the JSON for debugging purposes, `False` by default.
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
    json_data = parsed_solution

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
