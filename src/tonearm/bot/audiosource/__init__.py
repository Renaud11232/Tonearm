import nextcord
import threading
import subprocess


class SeekableFFmpegPCMAudio(nextcord.FFmpegPCMAudio):

    def __init__(self, source, *, executable="ffmpeg", pipe=False, stderr=subprocess.DEVNULL, before_options=None, options=None):
        super().__init__(
            source,
            executable=executable,
            pipe=pipe,
            stderr=stderr,
            before_options=before_options,
            options=options
        )
        self.__condition = threading.Condition()
        self.__chunks = []
        self.__next_chunk = 0
        threading.Thread(target=self.__read_all).start()

    def __read_chunk(self):
        chunk = super().read()
        with self.__condition:
            self.__chunks.append(chunk)
            self.__condition.notify()

    def __read_all(self):
        self.__read_chunk()
        while self.__chunks[-1] != b"":
            self.__read_chunk()

    def __is_finished_reading(self):
        len_chunks = len(self.__chunks)
        return len_chunks > 0 and self.__chunks[-1] == b""

    def read(self) -> bytes:
        with self.__condition:
            while not self.__is_finished_reading() and self.__next_chunk >= len(self.__chunks):
                self.__condition.wait()
            chunk = self.__chunks[self.__next_chunk]
            self.__next_chunk += 1
            return chunk

    @property
    def elapsed(self) -> int:
        return self.__next_chunk * 20

    @elapsed.setter
    def elapsed(self, elapsed: int):
        if elapsed < 0:
            raise ValueError("Elapsed time cannot be negative")
        with self.__condition:
            next_chunk = elapsed // 20
            if next_chunk >= len(self.__chunks):
                if self.__is_finished_reading():
                    raise ValueError("Elapsed time exceeds the total length of the track")
                else:
                    raise ValueError("Elapsed time exceeds the loaded portion of the track, wait for it to be loaded")
            self.__next_chunk = next_chunk
            self.__condition.notify()

class ControllableFFmpegPCMAudio(nextcord.PCMVolumeTransformer):

    def __init__(self, source, *, executable="ffmpeg", pipe=False, stderr=subprocess.DEVNULL, before_options=None, options=None):
        self.__source = SeekableFFmpegPCMAudio(
            source,
            executable=executable,
            pipe=pipe,
            stderr=stderr,
            before_options=before_options,
            options=options
        )
        super().__init__(self.__source)

    @property
    def elapsed(self) -> int:
        return self.__source.elapsed

    @elapsed.setter
    def elapsed(self, elapsed: int):
        self.__source.elapsed = elapsed
