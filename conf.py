import os
import yaml
from box import Box


CONFIG_PATH = 'config.yaml'


def load_config(config_path=CONFIG_PATH) -> Box:
    """
    Load the configuration from a YAML file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return Box(config, frozen_box=True)
