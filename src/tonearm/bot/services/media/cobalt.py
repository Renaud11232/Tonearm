from tonearm.cobalt import CobaltClient, CobaltException
from tonearm.exceptions import TonearmException
from .base import MediaServiceBase


class CobaltMediaService(MediaServiceBase):

    def __init__(self, cobalt_api_url: str, cobalt_api_key: str | None):
        super().__init__()
        self.__cobalt = CobaltClient(cobalt_api_url, cobalt_api_key)

    async def fetch(self, url: str) -> str:
        self._logger.debug(f"Fetching media via Cobalt API : {url}")
        try:
            response = self.__cobalt.process(
                url,
                audio_format="wav",
                download_mode="audio"
            )["url"]
            self._logger.debug(f"Cobalt API returned : {repr(response)}")
            return response
        except CobaltException as e:
            self._logger.warning(f"Cobalt API returned error : {repr(e)}")
            raise TonearmException(f"Unable to fetch media, Cobalt API returned `{str(e)}`")
