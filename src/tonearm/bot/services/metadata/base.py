from abc import ABC, abstractmethod
from typing import List
import logging

import googleapiclient.discovery

from tonearm.bot.data import TrackMetadata


class MetadataServiceBase(ABC):

    def __init__(self):
        self._logger = logging.getLogger("tonearm.metadata")

    @abstractmethod
    async def fetch(self, query: str) -> List[TrackMetadata]:
        pass

class YoutubeMetadataService(MetadataServiceBase, ABC):

    def __init__(self, api_key: str):
        super().__init__()
        self._youtube = googleapiclient.discovery.build(
            "youtube",
            "v3",
            developerKey=api_key
        )