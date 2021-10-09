import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "\\src")
from Utils.SizedQueue import *


class TestSizedQueue(unittest.TestCase):
    def test_put(self):
        q = SizedQueue(3)
        for i in range(3):
            q.put(i)

        for i in range(3):
            self.assertEqual(q[i], 2 - i)

    def test_iter(self):
        q = SizedQueue(3)
        for i in range(3):
            q.put(i)

        i = 2
        for elem in q:
            self.assertEqual(elem, i)
            i -= 1

    def test_over_put(self):
        q = SizedQueue(3)
        for i in range(4):
            q.put(i)

        with self.assertRaises(IndexError):
            for i in range(4):
                self.assertEqual(q[i], 3 - i)

    def test_pop(self):
        q = SizedQueue(3)
        for i in range(3):
            q.put(i)

        for i in range(3):
            self.assertEqual(q.pop(), i)

    def test_pop_from_empty(self):
        q = SizedQueue(1)
        with self.assertRaises(IndexError):
            q.pop()

    def test_full(self):
        q = SizedQueue(2)
        q.put(0)
        self.assertFalse(q.full())
        q.put(1)
        self.assertTrue(q.full())
        q.pop()
        self.assertFalse(q.full())


if __name__ == "__main__":
    unittest.main()
