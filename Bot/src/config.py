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


class ConfigManager(Singleton):
    def __init__(self):
        self._config = _load_config()

    def get_config(self, key: str = None):
        if key is not None:
            return self._config[key]
        return self._config

    def save_config(self, config: Dict, key: str = None):
        with open(os.path.join(PROJECT_DIR, "config.yml"), "w") as config_file:
            self._config[key] = config
            yaml.dump(self._config, config_file)
