import unittest
import sys
import os

SRC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src"
)
sys.path.append(SRC_DIR)
from Utils.LogClassifier import LogClassifier, LogType


class TestLogClassifier(unittest.TestCase):
    def expectEqual(self, first: any, second: any, msg: any, **params):
        with self.subTest(msg, **params):
            self.assertEqual(first, second)

    def setUp(self):
        self.classifier = LogClassifier(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../regex/test_regex.yml")
            )
        )

    def test_classify_logs(self):
        args = [
            "[11:23:31] [Test/Fatal] Error!\n",
            "[11:23:31] [Test/Log] hello world\n",
            "[11:23:31] [Test/Message] <wogns> 안녕하세요\n",
        ]

        result = [
            LogType.IGNORE,
            LogType.NORMAL,
            LogType.IMPORTANT,
        ]

        for a, r in zip(args, result):
            self.expectEqual(self.classifier.classify(a), r)
