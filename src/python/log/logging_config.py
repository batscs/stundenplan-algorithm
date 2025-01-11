import json
import logging.config
import os
from typing import Any

from utils import path_utils

LOGGING_CONFIG_PATH: str = os.path.join(
    path_utils.RESOURCES_PATH, "logging_config.json"
)
"""Path of the logging config file."""

LOGGING_FILE_PATH: str = os.path.join(path_utils.RESOURCES_PATH, "debug.log")
"""Path of the logging file."""


def configure_logging() -> None:
    """Configures the logging for the application.

    This function should only be called once at the start of the application.
    """
    with open(LOGGING_CONFIG_PATH) as logging_config_json:
        logging_config: dict[str, Any] = json.load(logging_config_json)
        # Fix logging filename to point to the correct location.
        logging_config["handlers"]["file"]["filename"] = LOGGING_FILE_PATH
        logging.config.dictConfig(logging_config)
