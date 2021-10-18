import unittest
import sys
import os

SRC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src"
)
sys.path.append(SRC_DIR)

from Cogs.ProgramManager import *

LOG_SIZE = 5
TEST_INP_PIPE_DIR = "/tmp/tip"
TEST_OUT_PIPE_DIR = "/tmp/top"


class TestProgramManagerCog(unittest.TestCase):
    def setUp(self):
        try:
            os.mkfifo(TEST_INP_PIPE_DIR)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                print(f"mkfifo fail, {oe.errno}", file=sys.stderr)
                raise oe
        try:
            os.mkfifo(TEST_OUT_PIPE_DIR)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                print(f"mkfifo fail, {oe.errno}", file=sys.stderr)
                raise oe

        self.manager = ProgramManager(LOG_SIZE, TEST_INP_PIPE_DIR, TEST_OUT_PIPE_DIR)
        self.ipipe = open(TEST_INP_PIPE_DIR, "r+b", buffering=0)
        self.opipe = open(TEST_OUT_PIPE_DIR, "r+b", buffering=0)
        # self.ctx = {"send" : }

    def tearDown(self):
        self.ipipe.close()
        self.opipe.close()
        self.manager.close_pipe()
        os.unlink(TEST_INP_PIPE_DIR)
        os.unlink(TEST_OUT_PIPE_DIR)

    def expectEqual(self, first: any, second: any, msg: any, **params):
        with self.subTest(msg, **params):
            self.assertEqual(first, second)

    def test_write_to_ipipe(self):
        string = "abcdefg\n"
        self.assertTrue(self.manager.write_command(string))
        self.assertEqual(self.ipipe.readline(len(string)).decode(), string)

    def test_read_from_opipe(self):
        strings = ["abcdefg\n", "hello world\n", "안녕하세요\n"]
        for s in strings:
            self.opipe.write(s.encode("utf-8"))

        for i in range(len(strings)):
            self.expectEqual(
                self.manager.log_cache[len(strings) - 1 - i],
                strings[i],
                "log cache must be equal to reversed string list",
            )


if __name__ == "__main__":
    unittest.main()
