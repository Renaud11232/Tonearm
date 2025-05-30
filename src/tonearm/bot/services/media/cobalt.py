from tonearm.cobalt import CobaltClient
from tonearm.exceptions import TonearmException
from .base import MediaServiceBase


class CobaltMediaService(MediaServiceBase):

    def __init__(self, cobalt_api_url: str, cobalt_api_key: str | None):
        super().__init__()
        self.__cobalt = CobaltClient(cobalt_api_url, cobalt_api_key)

    async def fetch(self, url: str) -> str:
        response = self.__cobalt.process(
            url,
            audio_format="wav",
            download_mode="audio"
        )
        if response["status"] == "error":
            raise TonearmException(f"Unable to fetch media, API returned `{response["error"]["code"]}`")
        return response["url"]
