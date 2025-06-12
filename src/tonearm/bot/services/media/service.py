import re
from collections import namedtuple

from injector import inject, singleton

from tonearm.bot.exceptions import TonearmException
from .base import MediaServiceBase
from .cobalt import CobaltMediaService
from .direct_url import DirectUrlMediaService

MediaServiceEntry = namedtuple("MediaServiceEntry", ["pattern", "service"])


@singleton
class MediaService(MediaServiceBase):

    @inject
    def __init__(self, cobalt_media_service: CobaltMediaService, direct_url_media_service: DirectUrlMediaService):
        super().__init__()
        self.__media_services = [
            MediaServiceEntry(r"^(?:https://)?youtube\.com(?:/.*)?$", cobalt_media_service),
            MediaServiceEntry(r"^(?:https://)?www\.youtube\.com(?:/.*)?$", cobalt_media_service),
            MediaServiceEntry(r"^(?:https://)?m\.youtube\.com(?:/.*)?$", cobalt_media_service),
            MediaServiceEntry(r"^(?:https://)?music\.youtube\.com(?:/.*)?$", cobalt_media_service),
            MediaServiceEntry(r"^(?:https://)?www\.music\.youtube\.com(?:/.*)?$", cobalt_media_service),
            MediaServiceEntry(r"^(?:https://)?youtu\.be(?:/.*)?$", cobalt_media_service),
            MediaServiceEntry(r"^https?://.*$", direct_url_media_service)
        ]

    async def fetch(self, url: str) -> str:
        for entry in self.__media_services:
            if re.search(entry.pattern, url):
                return await entry.service.fetch(url)
        self._logger.debug(f"No media service matched {url}")
        raise TonearmException(f"I'm unable to load this track, it's hosted on a service I don't support.")
