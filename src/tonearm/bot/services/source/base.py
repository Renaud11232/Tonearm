from abc import ABC, abstractmethod
import logging

from tonearm.bot.services.player.audiosource import ControllableFFmpegPCMAudio


class SourceServiceBase(ABC):

    def __init__(self):
        self._logger = logging.getLogger("tonearm.source")

    @abstractmethod
    def open(self, url: str) -> ControllableFFmpegPCMAudio:
        pass