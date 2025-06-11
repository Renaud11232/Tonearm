import re
from collections import namedtuple
from typing import List

from injector import inject

from tonearm.bot.data import TrackMetadata
from tonearm.bot.exceptions import TonearmException
from tonearm.configuration import Configuration
from .base import MetadataServiceBase
from .direct_url import DirectUrlMetadataService
from .youtube_search import YoutubeSearchMetadataService
from .youtube_url import YoutubeUrlMetadataService

MetadataServiceEntry = namedtuple("MetadataServiceEntry", ["pattern", "service"])

class MetadataService(MetadataServiceBase):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        self.__metadata_services = [
            MetadataServiceEntry(r"^(?:https://)youtube\.com(?:/.*)?$", YoutubeUrlMetadataService(configuration.youtube_api_key)),
            MetadataServiceEntry(r"^(?:https://)www\.youtube\.com(?:/.*)?$", YoutubeUrlMetadataService(configuration.youtube_api_key)),
            MetadataServiceEntry(r"^(?:https://)m\.youtube\.com(?:/.*)?$", YoutubeUrlMetadataService(configuration.youtube_api_key)),
            MetadataServiceEntry(r"^(?:https://)music\.youtube\.com(?:/.*)?$", YoutubeUrlMetadataService(configuration.youtube_api_key)),
            MetadataServiceEntry(r"^(?:https://)www\.music\.youtube\.com(?:/.*)?$", YoutubeUrlMetadataService(configuration.youtube_api_key)),
            MetadataServiceEntry(r"^(?:https://)youtu\.be(?:/.*)?$", YoutubeUrlMetadataService(configuration.youtube_api_key)),
            MetadataServiceEntry(r"^https?://.*$", DirectUrlMetadataService()),
            MetadataServiceEntry(r"^.*$", YoutubeSearchMetadataService(configuration.youtube_api_key))
        ]

    async def fetch(self, query: str) -> List[TrackMetadata]:
        for entry in self.__metadata_services:
            if re.search(entry.pattern, query):
                return await entry.service.fetch(query)
        self._logger.debug(f"No metadata service matched {query}")
        raise TonearmException("I'm unable to fetch this track, it's hosted on a service I don't support")
