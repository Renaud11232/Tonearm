from tonearm.cobalt import CobaltClient, CobaltException
from tonearm.exceptions import TonearmException
from .base import MediaServiceBase


class CobaltMediaService(MediaServiceBase):

    def __init__(self, cobalt_api_url: str, cobalt_api_key: str | None):
        super().__init__()
        self.__cobalt = CobaltClient(cobalt_api_url, cobalt_api_key)

    async def fetch(self, url: str) -> str:
        try:
            return self.__cobalt.process(
                url,
                audio_format="wav",
                download_mode="audio"
            )["url"]
        except CobaltException as e:
            raise TonearmException(f"Unable to fetch media, Cobalt API returned `{str(e)}`")
