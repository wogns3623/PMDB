import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "\\src")
from Utils.SizedQueue import *


class TestSizedQueue(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.queueSize = 3
        self.q = SizedQueue(self.queueSize)

    def fillUpQueue(self, queue: SizedQueue, size: int):
        for i in range(size):
            queue.put(i)

    def weakAssertEqual(self, first: any, second: any, msg: any, **params):
        with self.subTest(msg, **params):
            self.assertEqual(first, second)

    def test_put(self):
        self.fillUpQueue(self.q, self.queueSize)

        for i in range(self.queueSize):
            self.weakAssertEqual(self.q[i], 2 - i, "check item")

    def test_iter(self):
        self.fillUpQueue(self.q, self.queueSize)

        i = 2
        for item in self.q:
            self.weakAssertEqual(item, i, "check item")
            i -= 1

    def test_over_put(self):
        self.fillUpQueue(self.q, self.queueSize + 1)

        for i in range(3):
            self.weakAssertEqual(self.q[i], 3 - i, "check item")

        with self.assertRaises(IndexError):
            self.q[self.queueSize]

    def test_pop(self):
        self.fillUpQueue(self.q, self.queueSize)

        for i in range(3):
            self.weakAssertEqual(self.q.pop(), i, "check item")

    def test_pop_from_empty(self):
        with self.assertRaises(IndexError):
            self.q.pop()

    def test_full(self):
        self.assertFalse(self.q.full())
        self.fillUpQueue(self.q, self.queueSize)
        self.assertTrue(self.q.full())
        self.q.pop()
        self.assertFalse(self.q.full())


if __name__ == "__main__":
    unittest.main()
