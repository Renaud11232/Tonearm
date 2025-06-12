import subprocess
import logging
import threading

import nextcord

from .exceptions import PlayerException


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
        self.__logger = logging.getLogger("tonearm.audiosource")
        threading.Thread(target=self.__read_all).start()

    def __read_chunk(self):
        chunk = super().read()
        with self.__condition:
            self.__chunks.append(chunk)
            self.__condition.notify()

    def __read_all(self):
        self.__logger.debug(f"Started buffering audio in audio source {repr(self)}")
        self.__read_chunk()
        while self.__chunks[-1] != b"":
            self.__read_chunk()
        self.__logger.debug(f"Finished buffering audio in audio source {repr(self)}")

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
        self.__logger.debug(f"Got request to update elapsed time to {elapsed}ms in audio source {repr(self)}")
        if elapsed < 0:
            self.__logger.debug("Provided elapsed time is negative, using 0 instead")
            elapsed = 0
        with self.__condition:
            next_chunk = elapsed // 20
            self.__logger.debug(f"Requested elapsed time translates to chunk number {next_chunk}")
            if next_chunk >= len(self.__chunks):
                if self.__is_finished_reading():
                    self.__logger.debug(f"Chunk {next_chunk} does not exist in the track of length {len(self.__chunks)}, using the last chunk instead")
                    next_chunk = len(self.__chunks) - 1
                else:
                    self.__logger.debug(f"Chunk {next_chunk} is not loaded yet (current loaded length is {len(self.__chunks)})")
                    raise PlayerException("I’d love to seek there, but it’s still downloading... patience, friend")
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

