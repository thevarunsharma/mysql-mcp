import os
import yaml
from pydantic import BaseModel
from typing import Optional


class DbAuthSSLConfig(BaseModel):
    cert: str
    key: str
    ca: str


class DatabaseConfig(BaseModel):
    driver: str
    user: str
    password: str
    host: str
    database: str
    port: int
    ssl: Optional[DbAuthSSLConfig] = None


class Config(BaseModel):
    DATABASE: DatabaseConfig


CONFIG_PATH = 'config.yaml'


def load_config(config_path=CONFIG_PATH) -> Config:
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
    return Config(**config)
