from injector import singleton, inject

from tonearm.api.cobalt import CobaltClient, CobaltException
from tonearm.configuration import Configuration

from .base import MediaServiceBase
from .exceptions import MediaFetchingException


@singleton
class CobaltMediaService(MediaServiceBase):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        self.__cobalt = CobaltClient(configuration.cobalt_api_url, configuration.cobalt_api_key)

    def fetch(self, url: str) -> str:
        self._logger.debug(f"Fetching media via Cobalt API : {url}")
        try:
            return self.__cobalt.process(
                url,
                audio_format="wav",
                download_mode="audio"
            )["url"]
        except CobaltException as e:
            self._logger.warning(f"Cobalt API returned error : {repr(e)}")
            raise MediaFetchingException(f"Cobalt API returned error : `{str(e)}`")