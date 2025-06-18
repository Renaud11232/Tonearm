import threading

class AudioBuffer:

    def __init__(self, max_size: int, *, trim_size: int = 10_000):
        self.__max_size = max_size
        self.__trim_size = trim_size
        self.__chunks = []
        self.__head = 0
        self.__lock = threading.RLock()

    @property
    def max_size(self) -> int:
        return self.__max_size

    def append(self, chunk: bytes):
        with self.__lock:
            self.__chunks.append(chunk)
            if self.__max_size is not None and len(self) > self.__max_size:
                self.__head += 1
                if self.__head >= self.__trim_size:
                    self.__chunks = self.__chunks[self.__head:]
                    self.__head = 0
                return True
            return False

    def __getitem__(self, item):
        with self.__lock:
            length = len(self)
            if item < 0:
                item += length
            if item >= length:
                raise IndexError("buffer index out of range")
            return self.__chunks[item + self.__head]

    def __len__(self):
        with self.__lock:
            return len(self.__chunks) - self.__head