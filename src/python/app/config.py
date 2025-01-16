import os

from src.python.utils import path_utils

# DEFAULT CONFIGURATION
config = {
    "input": {
        "filename": "input.json"
      },
    "algorithm": {
        "generations": 50
    },
    "app": {
        "config": "stundenplan_config.json",
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

def get_path_input():
    filename = config["input"]["filename"]
    return os.path.join(path_utils.RESOURCE_INPUT_PATH, filename)

def get_algorithm_generations():
    return config["algorithm"]["generations"]


def get_path_config():
    return os.path.join(path_utils.RESOURCE_CONFIG_PATH, config["app"]["config"])


def get_config():
    return config


def get_server_allowed_ips():
    return config["app"]["server_allowed_ips"]