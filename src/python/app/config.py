import os

from src.python.utils import path_utils
from src.python.io import printer_json

# DEFAULT CONFIGURATION
config = {
    "algorithm": {
        "generations_max": 50
    },
    "application": {
        "filepath_config": "stundenplan_config.json",
        "filepath_input": "input.json",
        "server_allowed_ips": ["*"]
    }
}

def set_config(new_config):
    # sets new config for values that are provided, example only input -> filename -> FHW_DEV.json could be provided
    # so this info gets updated, but algorithm -> generations and all other values are not changed

    def update_dict(base_dict, updates):
        """
        Recursively updates a dictionary with values from another dictionary.
        """
        for key, value in updates.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                update_dict(base_dict[key], value)
            else:
                base_dict[key] = value

    update_dict(config, new_config)
    printer_json.save(config, get_application_path_config())

def get_path_input():
    filename = config["application"]["filepath_input"]
    return os.path.join(path_utils.RESOURCE_INPUT_PATH, filename)

def get_algorithm_generations_max():
    return config["algorithm"]["generations_max"]


def get_application_path_config():
    return os.path.join(path_utils.RESOURCE_CONFIG_PATH, config["application"]["filepath_config"])


def get_config():
    return config


def get_server_allowed_ips():
    return config["application"]["server_allowed_ips"]
