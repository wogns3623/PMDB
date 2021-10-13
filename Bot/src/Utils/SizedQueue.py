class SizedQueue:
    def __init__(self, max_size):
        self.__arr = []
        self.__max_size = max_size
        self.__start = 0
        self.__size = 0

    def __get_index(self, raw_index):
        return (self.__start + raw_index) % len(self.__arr)

    def __get_reversed_index(self, raw_index):
        return self.__get_index(self.__size - 1 - raw_index)

    def __getitem__(self, i):
        if i >= self.__size:
            raise IndexError("index must be lower then size of queue")
        return self.__arr[self.__get_reversed_index(i)]

    def __iter__(self):
        for i in range(self.__size):
            yield self.__arr[self.__get_reversed_index(i)]

    def full(self):
        return self.__max_size == self.__size

    def pop(self):
        if self.__size == 0:
            raise IndexError("pop from empty queue")
        ret = self.__arr[self.__start]
        self.__start = self.__get_index(1)
        self.__size -= 1
        return ret

    def put(self, element):
        if self.full():
            self.pop()
        if len(self.__arr) == self.__max_size:
            self.__arr[self.__get_index(self.__size)] = element
        else:
            self.__arr.append(element)
        self.__size += 1
