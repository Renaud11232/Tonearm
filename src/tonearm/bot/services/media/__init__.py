import re
from collections import namedtuple

from injector import inject, singleton

from tonearm.bot.exceptions import TonearmException
from tonearm.configuration import Configuration
from .base import MediaServiceBase
from .cobalt import CobaltMediaService

MediaServiceEntry = namedtuple("MediaServiceEntry", ["pattern", "service"])


@singleton
class MediaService(MediaServiceBase):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        self.__media_services = [
            MediaServiceEntry(r"^(?:https://)youtube\.com(?:/.*)?$", CobaltMediaService(configuration.cobalt_api_url, configuration.cobalt_api_key)),
            MediaServiceEntry(r"^(?:https://)www\.youtube\.com(?:/.*)?$", CobaltMediaService(configuration.cobalt_api_url, configuration.cobalt_api_key)),
            MediaServiceEntry(r"^(?:https://)m\.youtube\.com(?:/.*)?$", CobaltMediaService(configuration.cobalt_api_url, configuration.cobalt_api_key)),
            MediaServiceEntry(r"^(?:https://)music\.youtube\.com(?:/.*)?$", CobaltMediaService(configuration.cobalt_api_url, configuration.cobalt_api_key)),
            MediaServiceEntry(r"^(?:https://)www\.music\.youtube\.com(?:/.*)?$", CobaltMediaService(configuration.cobalt_api_url, configuration.cobalt_api_key)),
            MediaServiceEntry(r"^(?:https://)youtu\.be(?:/.*)?$", CobaltMediaService(configuration.cobalt_api_url, configuration.cobalt_api_key)),
        ]

    async def fetch(self, url: str) -> str:
        for entry in self.__media_services:
            if re.search(entry.pattern, url):
                return await entry.service.fetch(url)
        self._logger.debug(f"No media service matched {url}")
        raise TonearmException(f"Unable to fetch media from URL {url}, unsupported service")
