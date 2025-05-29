from typing import List

from tonearm.bot.data import TrackMetadata
from tonearm.exceptions import TonearmException
from .base import YoutubeMetadataService


class YoutubeSearchMetadataService(YoutubeMetadataService):

    def __init__(self, api_key: str | None):
        super().__init__(api_key)

    async def _fetch(self, query: str) -> List[TrackMetadata]:
        raise TonearmException("Not implemented yet")