from injector import singleton, inject
import yt_dlp
import nextcord

from tonearm.bot.services.source.exceptions import SourceOpeningException
from tonearm.bot.services.source.base import SourceServiceBase
from tonearm.configuration import Configuration

from tonearm.bot.services.player.audiosource import ControllableFFmpegPCMAudio


@singleton
class YoutubeSourceService(SourceServiceBase):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__()
        self.__configuration = configuration

    def open(self, url: str) -> nextcord.AudioSource:
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
        with yt_dlp.YoutubeDL(options) as ytdl:
            try:
                info = ytdl.extract_info(url, download=False)
                return ControllableFFmpegPCMAudio(
                    info["url"],
                    buffer_length=self.__configuration.buffer_length,
                    executable=self.__configuration.ffmpeg_executable
                )
            except yt_dlp.utils.DownloadError as e:
                raise SourceOpeningException(e.args[0])
