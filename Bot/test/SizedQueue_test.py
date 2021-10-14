import unittest
import sys
import os

SRC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "src"
)
sys.path.append(SRC_DIR)

from Utils.SizedQueue import *


class TestSizedQueue(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.queue_size = 3
        self.q = SizedQueue(self.queue_size)

    def expectEqual(self, first: any, second: any, msg: any, **params):
        with self.subTest(msg, **params):
            self.assertEqual(first, second)

    def fill_up_queue(self, queue: SizedQueue, size: int):
        for i in range(size):
            queue.put(i)

    def test_put(self):
        self.fill_up_queue(self.q, self.queue_size)

        for i in range(self.queue_size):
            self.expectEqual(self.q[i], 2 - i, "check item")

    def test_iter(self):
        self.fill_up_queue(self.q, self.queue_size)

        i = 2
        for item in self.q:
            self.expectEqual(item, i, "check item")
            i -= 1

    def test_over_put(self):
        self.fill_up_queue(self.q, self.queue_size + 1)

        for i in range(3):
            self.expectEqual(self.q[i], 3 - i, "check item")

        with self.assertRaises(IndexError):
            self.q[self.queue_size]

    def test_pop(self):
        self.fill_up_queue(self.q, self.queue_size)

        for i in range(3):
            self.expectEqual(self.q.pop(), i, "check item")

    def test_pop_from_empty(self):
        with self.assertRaises(IndexError):
            self.q.pop()

    def test_full(self):
        self.assertFalse(self.q.full())
        self.fill_up_queue(self.q, self.queue_size)
        self.assertTrue(self.q.full())
        self.q.pop()
        self.assertFalse(self.q.full())


if __name__ == "__main__":
    unittest.main()
