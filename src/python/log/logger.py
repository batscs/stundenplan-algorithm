import json
import logging.config
import os
from logging import Logger
from typing import Any
from src.python.utils import path_utils

LOGGING_CONFIG_PATH: str = os.path.join(path_utils.RESOURCE_CONFIG_PATH, "logging_config.json")
"""Path of the logging config file."""

_is_logging_configured = False

def configure_logging() -> None:
    """Configures the logging for the application.

    This function should only be called once at the start of the application.
    """
    global _is_logging_configured

    # Only configure logging if it hasn't been done already
    try:
        if not _is_logging_configured:
            with open(LOGGING_CONFIG_PATH) as logging_config_json:
                logging_config: dict[str, Any] = json.load(logging_config_json)
                logging.config.dictConfig(logging_config)

            _is_logging_configured = True  # Mark as configured
    except IOError:
        print("Logging config not found")

# call configure logging when module is imported
configure_logging()

logger_app: Logger = logging.getLogger("application")
logger_db: Logger = logging.getLogger("database")
logger_ga: Logger = logging.getLogger("algorithm")
