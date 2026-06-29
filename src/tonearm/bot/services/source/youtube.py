from injector import singleton, inject
import yt_dlp
import yt_dlp.utils
import discord
import requests
import time

from tonearm.bot.services.source.base import SourceServiceBase
from tonearm.configuration import Configuration
from tonearm.bot.exceptions import TranslatableException

from tonearm.bot.services.player.audiosource import ControllableFFmpegPCMAudio


@singleton
class YoutubeSourceService(SourceServiceBase):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        self.__configuration = configuration

    def open(self, url: str) -> discord.AudioSource:
        self._logger.debug(f"Fetching media from YouTube URL : {url}")
        options = {
            "format": "bestaudio",
            "logger": self._logger,
            "js_runtimes": {
                "deno": {}
            }
        }
        if self.__configuration.deno_executable != "deno":
            options["js_runtimes"]["deno"]["path"] = self.__configuration.deno_executable
        if self.__configuration.ffmpeg_executable != "ffmpeg":
            options.update({
                "ffmpeg_location": self.__configuration.ffmpeg_executable,
            })
        if self.__configuration.youtube_cookies is not None:
            options.update({
                "cookiefile": self.__configuration.youtube_cookies
            })
        try:
            with yt_dlp.YoutubeDL(options) as ytdl:
                info = ytdl.extract_info(url, download=False)
                url = info["url"]
                self.__wait_for_video(url)
                return ControllableFFmpegPCMAudio(
                    url,
                    buffer_length=self.__configuration.buffer_length,
                    executable=self.__configuration.ffmpeg_executable
                )
        except yt_dlp.utils.DownloadError as e:
            raise TranslatableException(e.args[0])

    def __wait_for_video(self, url: str):
        status_code = self.__get_status_code(url)
        retries = 0
        while status_code >= 400 and retries < 10:
            time.sleep(1)
            retries += 1
            status_code = self.__get_status_code(url)
        if status_code >= 400:
            raise TranslatableException(
                "YouTube video playback URL was not available (Error {status_code})",
                status_code=status_code
            )

    def __get_status_code(self, url: str):
        with requests.head(url) as response:
            self._logger.debug(f"Video URL {url} returned status code : {response.status_code}")
            return response.status_code
