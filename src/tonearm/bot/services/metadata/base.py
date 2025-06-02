from abc import ABC, abstractmethod
from typing import List
import logging

import googleapiclient.discovery

from tonearm.bot.data import TrackMetadata
from tonearm.exceptions import TonearmException


class MetadataServiceBase(ABC):

    def __init__(self):
        self._logger = logging.getLogger("tonearm.metadata")

    @abstractmethod
    async def fetch(self, query: str) -> List[TrackMetadata]:
        pass

class YoutubeMetadataService(MetadataServiceBase, ABC):

    def __init__(self, api_key: str | None):
        super().__init__()
        if api_key is None:
            self._youtube = None
        else:
            self._youtube = googleapiclient.discovery.build(
                "youtube",
                "v3",
                developerKey=api_key
            )

    async def fetch(self, query: str) -> List[TrackMetadata]:
        if self._youtube is None:
            self._logger.warning("Unable to use YouTube API, no API key have been set")
            raise TonearmException("No YouTube API key provided")
        return await self._fetch(query)

    @abstractmethod
    async def _fetch(self, query: str) -> List[TrackMetadata]:
        pass