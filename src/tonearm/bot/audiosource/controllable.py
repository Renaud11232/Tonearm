import subprocess

import nextcord

from .seekable import SeekableFFmpegPCMAudio


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


