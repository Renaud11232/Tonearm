import re
from collections import namedtuple

from tonearm.exceptions import TonearmException
from .base import MediaServiceBase
from .cobalt import CobaltMediaService

MediaServiceEntry = namedtuple("MediaServiceEntry", ["pattern", "service"])

class MediaService(MediaServiceBase):

    def __init__(self, cobalt_api_url: str, cobalt_api_key: str | None):
        super().__init__()
        self.__media_services = [
            MediaServiceEntry(r"^(?:https://)www\.youtube\.com(?:/.*)?$", CobaltMediaService(cobalt_api_url, cobalt_api_key))
        ]

    async def fetch(self, url: str) -> str:
        for entry in self.__media_services:
            if re.search(entry.pattern, url):
                return await entry.service.fetch(url)
        raise TonearmException(f"Unable to fetch media from URL {url}, unsupported service")
