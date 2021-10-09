class SizedQueue:
    def __init__(self, max_size):
        self.__arr = []
        self.__max_size = max_size
        self.__start = 0
        self.__size = 0

    def __getIndex(self, raw_index):
        return (self.__start + raw_index) % len(self.__arr)

    def __getReversedIndex(self, raw_index):
        return self.__getIndex(self.__size - 1 - raw_index)

    def __getitem__(self, i):
        if i >= self.__size:
            raise IndexError("index must be lower then size of queue")
        return self.__arr[self.__getReversedIndex(i)]

    def __iter__(self):
        for i in range(self.__size):
            yield self.__arr[self.__getReversedIndex(i)]

    def full(self):
        return self.__max_size == self.__size

    def pop(self):
        if self.__size == 0:
            raise IndexError("pop from empty queue")
        ret = self.__arr[self.__start]
        self.__start = self.__getIndex(1)
        self.__size -= 1
        return ret

    def put(self, element):
        if self.full():
            self.pop()
        if len(self.__arr) == self.__max_size:
            self.__arr[self.__getIndex(self.__size)] = element
        else:
            self.__arr.append(element)
        self.__size += 1
