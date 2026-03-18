from abc import ABC, abstractmethod
import logging

import discord


class SourceServiceBase(ABC):

    def __init__(self):
        self._logger = logging.getLogger("tonearm.source")

    @abstractmethod
    def open(self, url: str) -> discord.AudioSource:
        pass