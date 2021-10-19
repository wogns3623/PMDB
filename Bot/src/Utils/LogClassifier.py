from typing import List
from enum import Enum

import yaml
import re


class LogType(Enum):
    IGNORE = 0
    NORMAL = 1
    IMPORTANT = 2


class LogClassifier:
    def __init__(self, path: str):
        """Create log classifier instance.

        Args:
            path (str): classifier regex file path.
        """
        self.__classifier_regex = []
        self.load_classifier(path)
        pass

    def load_classifier(self, path: str) -> None:
        """load classifier regex list from given path.

        Args:
            path (str): classifier path.
        """
        with open(path) as regex_file:
            regex_list = yaml.load(regex_file, Loader=yaml.FullLoader)["regex"]
        pass

    def classify(self, log: str) -> LogType:
        pass
