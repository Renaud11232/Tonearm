from injector import singleton, inject

import nextcord

from tonearm.configuration import Configuration
from .base import SourceServiceBase
from tonearm.bot.services.player.audiosource import ControllableFFmpegPCMAudio


@singleton
class DirectUrlSourceService(SourceServiceBase):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        self.__configuration = configuration

    def open(self, url: str) -> nextcord.AudioSource:
        return ControllableFFmpegPCMAudio(
            url,
            buffer_length=self.__configuration.buffer_length,
            executable=self.__configuration.ffmpeg_executable
        )