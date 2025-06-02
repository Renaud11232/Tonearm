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
        self.__lock = threading.Lock()
        self.__chunks = []
        self.__next_chunk = 0

    def read(self) -> bytes:
        with self.__lock:
            while self.__next_chunk >= len(self.__chunks) and (len(self.__chunks) == 0 or self.__chunks[-1] != b""):
                self.__chunks.append(super().read())
            if self.__next_chunk < len(self.__chunks):
                chunk = self.__chunks[self.__next_chunk]
                self.__next_chunk += 1
                return chunk
            else:
                return self.__chunks[-1]

    @property
    def elapsed(self) -> int:
        return self.__next_chunk * 20

    @elapsed.setter
    def elapsed(self, elapsed: int):
        with self.__lock:
            self.__next_chunk = elapsed // 20

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
