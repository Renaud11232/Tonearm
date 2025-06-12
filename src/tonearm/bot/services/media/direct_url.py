from injector import singleton

from tonearm.bot.exceptions import TonearmException

from .base import MediaServiceBase


@singleton
class DirectUrlMediaService(MediaServiceBase):

    def __init__(self):
        super().__init__()

    async def fetch(self, url: str) -> str:
        self._logger.debug(f"Fetching media from direct url : {url}")
        #TODO
        raise TonearmException("Not implemented yet")