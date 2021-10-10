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

    def test_put(self):
        self.fillUpQueue(self.q, self.queueSize)

        for i in range(self.queueSize):
            with self.subTest("check item", i=i):
                self.assertEqual(self.q[i], 2 - i)

    def test_iter(self):
        self.fillUpQueue(self.q, self.queueSize)

        i = 2
        for elem in self.q:
            with self.subTest("check item", i=i):
                self.assertEqual(elem, i)
            i -= 1

    def test_over_put(self):
        self.fillUpQueue(self.q, self.queueSize + 1)

        for i in range(3):
            with self.subTest("check item", i=i):
                self.assertEqual(self.q[i], 3 - i)

        with self.subTest("check index error raised"):
            with self.assertRaises(IndexError):
                self.q[self.queueSize]

    def test_pop(self):
        self.fillUpQueue(self.q, self.queueSize)

        for i in range(3):
            with self.subTest("check item", i=i):
                self.assertEqual(self.q.pop(), i)

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
