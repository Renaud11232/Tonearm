from typing import List
import html

from tonearm.bot.data import TrackMetadata
from tonearm.exceptions import TonearmException
from .base import YoutubeMetadataService


class YoutubeSearchMetadataService(YoutubeMetadataService):

    def __init__(self, api_key: str | None):
        super().__init__(api_key)

    async def _fetch(self, query: str) -> List[TrackMetadata]:
        response = self._youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=1
        ).execute()
        if "items" not in response and len(response["items"]) == 0:
            raise TonearmException("No YouTube video found for those keywords")
        return [
            TrackMetadata(
                url=f"https://www.youtube.com/watch?v={response["items"][0]["id"]["videoId"]}",
                title=html.unescape(response["items"][0]["snippet"]["title"])
            )
        ]