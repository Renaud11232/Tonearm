from abc import ABC, abstractmethod
import logging


class MediaServiceBase(ABC):

    def __init__(self):
        self._logger = logging.getLogger("tonearm.media")

    @abstractmethod
    def fetch(self, url: str) -> str:
        pass