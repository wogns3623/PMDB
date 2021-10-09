import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "\\src")
from Cogs.ProgramManager import *


class TestProgramManager(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()


if __name__ == "__main__":
    unittest.main()
