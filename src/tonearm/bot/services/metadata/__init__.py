import re
from collections import namedtuple
from typing import List

from tonearm.bot.data import TrackMetadata
from tonearm.exceptions import TonearmException
from .base import MetadataServiceBase
from .direct_url import DirectUrlMetadataService
from .youtube_search import YoutubeSearchMetadataService
from .youtube_url import YoutubeUrlMetadataService

MetadataServiceEntry = namedtuple("MetadataServiceEntry", ["pattern", "service"])

class MetadataService(MetadataServiceBase):

    def __init__(self, youtube_api_key: str | None):
        super().__init__()
        self.__metadata_services = [
            MetadataServiceEntry(r"^(?:https://)?(?:youtu\.be|(?:(?:www\.)?(?:music\.)|m\.)?youtube\.com)(?:/.*)?$", YoutubeUrlMetadataService(youtube_api_key)),
            MetadataServiceEntry(r"^https?://.*$", DirectUrlMetadataService()),
            MetadataServiceEntry(r"^.*$", YoutubeSearchMetadataService(youtube_api_key))
        ]

    async def fetch(self, query: str) -> List[TrackMetadata]:
        for entry in self.__metadata_services:
            if re.search(entry.pattern, query):
                return await entry.service.fetch(query)
        raise TonearmException("I'm unable to fetch this track, it's hosted on a service I don't support")
