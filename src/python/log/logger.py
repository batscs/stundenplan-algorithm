import json
import logging.config
import os
from io import StringIO
from logging import Logger
from src.python.utils import path_utils
from src.python.io import reader_json

LOGGING_CONFIG_PATH: str = os.path.join(path_utils.RESOURCE_CONFIG_PATH, "logging_config.json")
"""Path of the logging config file."""

_is_logging_configured = False

formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

stream_log_algorithm = StringIO()
stream_log_application = StringIO()
stream_log_server = StringIO()

stream_handler_algorithm = logging.StreamHandler(stream_log_algorithm)
stream_handler_application = logging.StreamHandler(stream_log_application)
stream_handler_server = logging.StreamHandler(stream_log_server)

stream_handler_algorithm.setFormatter(formatter)
stream_handler_application.setFormatter(formatter)
stream_handler_server.setFormatter(formatter)

def configure_logging() -> None:
    """Configures the logging for the application.

    This function should only be called once at the start of the application.
    """
    global _is_logging_configured

    # Only configure logging if it hasn't been done already
    try:
        if not _is_logging_configured:

            json_config = reader_json.parse(LOGGING_CONFIG_PATH)

            if json_config is not None:
                logging.config.dictConfig(json_config)

            _is_logging_configured = True  # Mark as configured
    except IOError:
        print("Logging config not found")

# call configure logging when module is imported
configure_logging()

logger_app: Logger = logging.getLogger("application")
logger_ga: Logger = logging.getLogger("algorithm")
logger_srv: Logger = logging.getLogger("server")

logger_ga.addHandler(stream_handler_algorithm)
logger_app.addHandler(stream_handler_application)
logger_srv.addHandler(stream_handler_server)

def get_logs_algorithm():
    return stream_log_algorithm.getvalue()

def get_logs_application():
    return stream_log_application.getvalue()

def get_logs_server():
    return stream_log_server.getvalue()