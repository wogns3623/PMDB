import os
import yaml
from typing import Dict

from Utils.designpattern import Singleton

PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
SOURCE_DIR = os.path.join(PROJECT_DIR, "src")


def _load_config():
    with open(os.path.join(PROJECT_DIR, "config.yml")) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)["config"]
        return config


class ConfigManager:
    _config = _load_config()

    @classmethod
    def get_config(cls, key: str = None):
        if key is not None:
            return cls._config[key]
        return cls._config

    @classmethod
    def save_config(cls, config: Dict, key: str = None):
        with open(os.path.join(PROJECT_DIR, "config.yml"), "w") as config_file:
            cls._config[key] = config
            yaml.dump(cls._config, config_file)
