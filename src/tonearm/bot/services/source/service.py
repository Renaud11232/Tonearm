import re
from dataclasses import dataclass

from injector import inject, singleton
import nextcord

from .base import SourceServiceBase
from .direct_url import DirectUrlSourceService
from .exceptions import SourceOpeningException
from .youtube import YoutubeSourceService


@dataclass
class SourceServiceEntry:
    pattern: str
    service: SourceServiceBase


@singleton
class SourceService(SourceServiceBase):

    @inject
    def __init__(self, youtube_source_service: YoutubeSourceService, direct_url_source_service: DirectUrlSourceService):
        super().__init__()
        self.__source_services = [
            SourceServiceEntry(r"^(?:https://)?youtube\.com(?:/.*)?$", youtube_source_service),
            SourceServiceEntry(r"^(?:https://)?www\.youtube\.com(?:/.*)?$", youtube_source_service),
            SourceServiceEntry(r"^(?:https://)?m\.youtube\.com(?:/.*)?$", youtube_source_service),
            SourceServiceEntry(r"^(?:https://)?music\.youtube\.com(?:/.*)?$", youtube_source_service),
            SourceServiceEntry(r"^(?:https://)?www\.music\.youtube\.com(?:/.*)?$", youtube_source_service),
            SourceServiceEntry(r"^(?:https://)?youtu\.be(?:/.*)?$", youtube_source_service),
            SourceServiceEntry(r"^https?://.*$", direct_url_source_service)
        ]

    def open(self, url: str) -> nextcord.AudioSource:
        for entry in self.__source_services:
            if re.search(entry.pattern, url):
                return entry.service.open(url)
        self._logger.debug(f"No source service matched {url}")
        raise SourceOpeningException(
            "I could not load the track, it's hosted on a service I don't support."
        )
