from injector import singleton

from .base import MediaServiceBase
from .exceptions import MediaFetchingException


@singleton
class DirectUrlMediaService(MediaServiceBase):

    def __init__(self):
        super().__init__()

    async def fetch(self, url: str) -> str:
        self._logger.debug(f"Fetching media from direct url : {url}")
        #TODO
        raise MediaFetchingException("Direct URLs are not supported yet")