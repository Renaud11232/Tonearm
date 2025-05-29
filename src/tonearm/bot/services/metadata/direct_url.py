from typing import List

from tonearm.bot.data import TrackMetadata
from tonearm.exceptions import TonearmException
from .base import MetadataServiceBase


class DirectUrlMetadataService(MetadataServiceBase):

    def __init__(self):
        super().__init__()

    async def fetch(self, query: str) -> List[TrackMetadata]:
        raise TonearmException("Not implemented yet")