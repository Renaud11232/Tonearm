import re
from collections import namedtuple
from typing import List

from injector import inject, singleton

from .base import MetadataServiceBase
from .metadata import TrackMetadata
from .direct_url import DirectUrlMetadataService
from .youtube_search import YoutubeSearchMetadataService
from .youtube_url import YoutubeUrlMetadataService
from .exceptions import MetadataFetchingException


MetadataServiceEntry = namedtuple("MetadataServiceEntry", ["pattern", "service"])


@singleton
class MetadataService(MetadataServiceBase):

    @inject
    def __init__(self,
                 youtube_url_metadata_service: YoutubeUrlMetadataService,
                 direct_url_metadata_service: DirectUrlMetadataService,
                 youtube_search_metadata_service: YoutubeSearchMetadataService):
        super().__init__()
        self.__metadata_services = [
            MetadataServiceEntry(r"^(?:https://)?youtube\.com(?:/.*)?$", youtube_url_metadata_service),
            MetadataServiceEntry(r"^(?:https://)?www\.youtube\.com(?:/.*)?$", youtube_url_metadata_service),
            MetadataServiceEntry(r"^(?:https://)?m\.youtube\.com(?:/.*)?$", youtube_url_metadata_service),
            MetadataServiceEntry(r"^(?:https://)?music\.youtube\.com(?:/.*)?$", youtube_url_metadata_service),
            MetadataServiceEntry(r"^(?:https://)?www\.music\.youtube\.com(?:/.*)?$", youtube_url_metadata_service),
            MetadataServiceEntry(r"^(?:https://)?youtu\.be(?:/.*)?$", youtube_url_metadata_service),
            MetadataServiceEntry(r"^https?://.*$", direct_url_metadata_service),
            MetadataServiceEntry(r"^.*$", youtube_search_metadata_service)
        ]

    def fetch(self, query: str) -> List[TrackMetadata]:
        for entry in self.__metadata_services:
            if re.search(entry.pattern, query):
                return entry.service.fetch(query)
        self._logger.debug(f"No metadata service matched {query}")
        raise MetadataFetchingException("I'm unable to fetch this track, it's hosted on a service I don't support.")
