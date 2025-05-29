import re
from urllib.parse import urlparse, parse_qs
from typing import List
import html

from tonearm.bot.data import TrackMetadata
from tonearm.exceptions import TonearmException
from .base import YoutubeMetadataService


class YoutubeUrlMetadataService(YoutubeMetadataService):

    def __init__(self, api_key: str | None):
        super().__init__(api_key)

    async def _fetch(self, query: str) -> List[TrackMetadata]:
        parsed_url = urlparse(query)
        if "list" not in parse_qs(parsed_url.query) or len(parse_qs(parsed_url.query)["list"]) == 0:
            return await self.__fetch_video(self.__get_video_id(query))
        else:
            return await self.__fetch_playlist(parse_qs(parsed_url.query)["list"][0])

    @staticmethod
    def __get_video_id(url: str):
        regex = re.compile(r"(?:v=|/)([0-9A-Za-z_-]{11}).*")
        results = regex.search(url)
        if not results:
            raise TonearmException("Unable to extract the video ID from the URL")
        return results.group(1)

    async def __fetch_video(self, video: str) -> List[TrackMetadata]:
        response = self._youtube.videos().list(
            part="snippet",
            id=video,
            maxResults=1
        ).execute()
        if "items" not in response and len(response["items"]) == 0:
            raise TonearmException("The requested track was not found on YouTube")
        return [
            TrackMetadata(
                url=f"https://www.youtube.com/watch?v={video}",
                title=html.unescape(response["items"][0]["snippet"]["title"])
            )
        ]

    async def __fetch_playlist(self, playlist: str) -> List[TrackMetadata]:
        response = self._youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist,
            maxResults=50
        ).execute()
        if "items" not in response and len(response["items"]) == 0:
            raise TonearmException("The requested playlist was not found on YouTube")
        return [
            TrackMetadata(
                url=f"https://www.youtube.com/watch?v={item["snippet"]["resourceId"]["videoId"]}",
                title=html.unescape(item["snippet"]["title"])
            ) for item in response["items"]
        ]