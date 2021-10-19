import os
import yaml
from typing import Dict

from Utils.designpattern import Singleton

PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
SOURCE_DIR = os.path.join(PROJECT_DIR, "src")


class ConfigManager(Singleton):
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        with open(os.path.join(PROJECT_DIR, "config.yml")) as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            return config

    def save_config(self):
        with open(os.path.join(PROJECT_DIR, "config.yml"), "w") as config_file:
            yaml.safe_dump(self.config, config_file)
