import re
from urllib.parse import urlparse, parse_qs
from typing import List
import html

from injector import singleton, inject

from tonearm.bot.exceptions import TonearmException
from tonearm.configuration import Configuration
from .base import YoutubeMetadataService
from .metadata import TrackMetadata


@singleton
class YoutubeUrlMetadataService(YoutubeMetadataService):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__(configuration)

    async def fetch(self, query: str) -> List[TrackMetadata]:
        self._logger.debug(f"Fetching metadata via YouTube API : {query}")
        if self.__is_playlist(query):
            return await self.__fetch_playlist(query)
        else:
            return await self.__fetch_video(query)

    @staticmethod
    def __is_playlist(url: str) -> bool:
        parsed_qs = parse_qs(urlparse(url).query)
        return "list" in parsed_qs and len(parsed_qs["list"]) > 0

    @staticmethod
    def __get_playlist_id(url: str):
        return parse_qs(urlparse(url).query)["list"][0]

    @staticmethod
    def __get_video_id(url: str):
        regex = re.compile(r"(?:v=|/)([0-9A-Za-z_-]{11}).*")
        results = regex.search(url)
        if not results:
            raise TonearmException("Unable to extract the video ID from the URL")
        return results.group(1)

    async def __fetch_video(self, url: str) -> List[TrackMetadata]:
        id = self.__get_video_id(url)
        self._logger.debug(f"Fetching metadata via YouTube Videos API for video id : {id}")
        response = self._youtube.videos().list(
            part="snippet",
            id=id,
            maxResults=1
        ).execute()
        return [
            TrackMetadata(
                url=url,
                title=html.unescape(item["snippet"]["title"])
            ) for item in response["items"]
        ]

    async def __fetch_playlist(self, url: str) -> List[TrackMetadata]:
        id = self.__get_playlist_id(url)
        self._logger.debug(f"Fetching metadata via YouTube Playlist Items API for playlist id : {id}")
        response = self._youtube.playlistItems().list(
            part="snippet",
            playlistId=id,
            maxResults=50
        ).execute()
        return [
            TrackMetadata(
                url=f"https://www.youtube.com/watch?v={item["snippet"]["resourceId"]["videoId"]}",
                title=html.unescape(item["snippet"]["title"])
            ) for item in response["items"]
        ]