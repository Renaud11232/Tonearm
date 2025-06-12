from typing import List

from injector import singleton

from tonearm.bot.exceptions import TonearmException

from .base import MetadataServiceBase
from .metadata import TrackMetadata


@singleton
class DirectUrlMetadataService(MetadataServiceBase):

    def __init__(self):
        super().__init__()

    async def fetch(self, query: str) -> List[TrackMetadata]:
        self._logger.debug(f"Fetching metadata for direct url : {query}")
        #TODO
        raise TonearmException("Not implemented yet")