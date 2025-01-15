import json
from typing import Any

def parse(json_file_path: str):
    """Parses a JSON file into the database.

    Args:
        json_file_path: Path to the JSON file to parse the data from,
                        by default the path of the standard JSON file DEFAULT_JSON_FILE_PATH.

    Raises:
        FileNotFoundError: If json_file_path does not exist.
        ValueError: If the JSON file has an invalid structure.
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            data: dict[str, list[dict[str, Any]]] = json.load(json_file)

        return data
    except IOError:
        return None