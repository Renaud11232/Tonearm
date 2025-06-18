import subprocess
import logging
import threading
import math

import nextcord

from .exceptions import PlayerException
from .buffer import AudioBuffer


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
        self.__offset = 0
        self.__next_chunk = 0
        self.__chunks = AudioBuffer((1_000 // 20) * 60 * 60 * 2) # 2 hours of audio
        self.__logger = logging.getLogger("tonearm.audiosource")
        self.__buffering_stopped = False
        self.__buffering_thread = threading.Thread(target=self.__buffer_all)
        self.__buffering_thread.start()

    def __buffer_chunk(self):
        chunk = super().read()
        with self.__condition:
            while not self.__buffering_stopped and len(self.__chunks) - self.__next_chunk + self.__offset > self.__chunks.max_size // 2:
                self.__condition.wait()
            if not self.__buffering_stopped:
                if self.__chunks.append(chunk):
                    self.__offset += 1
                self.__condition.notify()

    def __buffer_all(self):
        self.__logger.debug(f"Started buffering audio in audio source {repr(self)}")
        self.__buffer_chunk()
        while not self.__buffering_stopped and self.__chunks[-1] != b"":
            self.__buffer_chunk()
        if self.__buffering_stopped:
            self.__logger.debug(f"Buffering explicitly stopped in audio source {repr(self)}")
        else:
            self.__logger.debug(f"Finished buffering normally in audio source {repr(self)}")

    def __is_finished_buffering(self):
        return len(self.__chunks) > 0 and self.__chunks[-1] == b""

    def read(self) -> bytes:
        with self.__condition:
            while not self.__is_finished_buffering() and self.__next_chunk - self.__offset >= len(self.__chunks):
                self.__condition.wait()
            chunk = self.__chunks[self.__next_chunk - self.__offset]
            self.__next_chunk += 1
            self.__condition.notify()
            return chunk

    @property
    def elapsed(self) -> int:
        return self.__next_chunk * 20

    @property
    def total(self):
        with self.__condition:
            if self.__is_finished_buffering():
                return (len(self.__chunks) + self.__offset) * 20
            else:
                return math.inf

    @elapsed.setter
    def elapsed(self, elapsed: int):
        next_chunk = elapsed // 20
        self.__logger.debug(f"Got request to update elapsed time to {elapsed}ms (chunk {next_chunk}) in audio source {repr(self)}")
        with self.__condition:
            if next_chunk - self.__offset < 0:
                self.__logger.debug("Provided elapsed time is before the start of the buffer")
                raise PlayerException("That’s too far back ! Even my buffer’s got limits.")
            if next_chunk - self.__offset >= len(self.__chunks):
                self.__logger.debug(f"Chunk {next_chunk} does not exist in buffer of {len(self.__chunks)} with offset {self.__offset}")
                if self.__is_finished_buffering():
                    raise PlayerException("I’d love to seek there, but the track isn't that long.")
                else:
                    raise PlayerException("I’d love to seek there, but it’s still downloading... patience, friend")
            self.__next_chunk = next_chunk
            self.__condition.notify()

    def cleanup(self) -> None:
        with self.__condition:
            self.__buffering_stopped = True
            self.__condition.notify_all()
        super().cleanup()


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

    @property
    def total(self):
        return self.__source.total

