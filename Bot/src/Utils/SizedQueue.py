class SizedQueue:
    def __init__(self, max_size=2):
        # self.__arr = [None] * max___size
        self.__arr = []
        self.__max___size = max_size
        self.__start = 0
        self.__size = 0

    def __getitem__(self, key):
        return self.__arr[self.__getIndex(key)]

    def __iter__(self):
        for i in range(self.__size):
            print(self.__getIndex(self.__start + i), end=", ")
            yield self.__arr[self.__getIndex(self.__start + i)]

    # get element of given index
    def __getIndex(self, raw_index):
        return (raw_index) % len(self.__arr)

    # # move cursor toward
    # def __moveCursor(self, cursor):
    #     return (cursor + 1) % len(self.__arr)

    def full(self):
        return self.__max___size == self.__size

    def pop(self):
        if self.__size == 0:
            raise IndexError("pop from empty queue")
        self.__start = self.__getIndex(self.__start + 1)
        self.__size -= 1
        return self.__arr[self.__start]

    def put(self, element):
        if self.full():
            self.pop()
        if len(self.__arr) == self.__max___size:
            self.__arr[self.__getIndex(self.__start + self.__size)] = element
        else:
            self.__arr.append(element)
        self.__size += 1
