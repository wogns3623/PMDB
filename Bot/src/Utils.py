import sys
import time


def get_local_time():
    t = time.localtime()
    return f"{t.tm_hour}:{t.tm_min}:{t.tm_sec}"


def log(message):
    print(f"[{get_local_time()}] [Bot/Info] {message}")


def errlog(message):
    print(f"[{get_local_time()}] [Bot/Error] {message}", file=sys.stderr)


class SizedQueue:
    def __init__(self, max_size=2):
        # self.arr = [None] * max_size
        self.arr = []
        self.__max_size = max_size
        self.start = 0
        self.size = 0

    def __iter__(self):
        for i in range(self.size):
            print(self.__getIndex(self.start + i), end=", ")
            yield self.arr[self.__getIndex(self.start + i)]

    # get element of given index
    def __getIndex(self, raw_index):
        return (raw_index) % len(self.arr)

    # move cursor toward
    def __moveCursor(self, cursor):
        return (cursor + 1) % len(self.arr)

    def full(self):
        return self.__max_size == self.size

    def pop(self):
        if self.size == 0:
            raise IndexError("pop from empty queue")
        self.start = self.__moveCursor(self.start)
        self.size -= 1
        return self.arr[self.start]

    def put(self, element):
        if self.full():
            self.pop()
        if len(self.arr) == self.__max_size:
            self.arr[self.__getIndex(self.start + self.size)] = element
        else:
            self.arr.append(element)
        self.size += 1


if __name__ == "__main__":
    q = SizedQueue(10)
    for i in range(5):
        q.put((i + 1) * 10)
        print(f"start: {q.start}, size: {q.size}, arr: {[i for i in q]}\n")
    print("pop")
    q.pop()
    print(f"start: {q.start}, size: {q.size}, arr: {[i for i in q]}\n")
    for i in range(5, 20):
        q.put((i + 1) * 10)
        print(f"start: {q.start}, size: {q.size}, arr: {[i for i in q]}\n")
