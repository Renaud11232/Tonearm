from injector import singleton, inject
import yt_dlp

from tonearm.bot.services.media.base import MediaServiceBase
from tonearm.configuration import Configuration


@singleton
class YoutubeMediaService(MediaServiceBase):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        self.__configuration = configuration

    def fetch(self, url: str) -> str:
        self._logger.debug(f"Fetching media from YouTube URL : {url}")
        options = {
            "format": "bestaudio",
            "logger": self._logger
        }
        if self.__configuration.ffmpeg_executable != "ffmpeg":
            options.update({
                "ffmpeg-location": self.__configuration.ffmpeg_executable,
            })
        if self.__configuration.youtube_cookies is not None:
            options.update({
                "cookies": self.__configuration.youtube_cookies
            })
        with yt_dlp.YoutubeDL(options) as ytdl:
            info = ytdl.extract_info(url, download=False)
            return info["url"] #TODO: handle the case where this key doesn't exists + update translations
