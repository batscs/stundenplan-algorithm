import json
import os
import re
from typing import Any, Dict
import pandas as pd
from pandas import DataFrame
from src.python.utils import path_utils
from src.python.api import api

JSON_FILE_NAME: str = path_utils.INPUT_JSON_FILENAME
"""Name of the excel file to parse."""

DEFAULT_JSON_FILE_PATH: str = os.path.join(path_utils.RESOURCE_INPUT_PATH, JSON_FILE_NAME)
"""Default path of the excel file containing the data to parse."""

def _convert_to_dataframe(data: list[dict[str, Any]]) -> DataFrame:
    df = pd.DataFrame(data)

    # Regex pattern to match strings with a colon but no alphabetic characters or underscores
    time_pattern = r'^[^a-zA-Z_]*:[^a-zA-Z_]*$'

    # Normalize time columns to match Excel-parsed data (convert HH:MM:SS to minutes).
    for column in df.columns:
        if df[column].dtype == "object" and df[column].str.contains(":").any():
            if re.match(time_pattern, df[column].to_string()):
                # Apply the time conversion only if the value matches the time format pattern
                df[column] = df[column].apply(lambda t: _time_to_minutes(t) if isinstance(t, str) else None)
            else:
                df[column] = df[column].astype(str)

    return df


def _time_to_minutes(time_str: str) -> int:
    """Converts a time string (HH:MM:SS) to minutes since midnight."""
    hours, minutes, _ = map(int, time_str.split(":"))
    return hours * 60 + minutes


def parse(
    json_file_path: str = DEFAULT_JSON_FILE_PATH,
    fast_and_least_verbose: bool = True,
) -> None:
    """Parses a JSON file into the database.

    Args:
        json_file_path: Path to the JSON file to parse the data from,
                        by default the path of the standard JSON file DEFAULT_JSON_FILE_PATH.
        fast_and_least_verbose: Whether parsing should be done in the fastest and least verbose way,
                                by default True.

    Raises:
        FileNotFoundError: If json_file_path does not exist.
        ValueError: If the JSON file has an invalid structure.
    """
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        data: dict[str, list[dict[str, Any]]] = json.load(json_file)

    api.inject(data)