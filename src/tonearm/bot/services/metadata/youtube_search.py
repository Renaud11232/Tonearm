from typing import List
import html

from injector import singleton, inject

import googleapiclient.errors

from tonearm.configuration import Configuration
from .exceptions import MetadataFetchingException
from .base import YoutubeMetadataService
from .metadata import TrackMetadata


@singleton
class YoutubeSearchMetadataService(YoutubeMetadataService):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__(configuration)

    def fetch(self, query: str) -> List[TrackMetadata]:
        self._logger.debug(f"Fetching metadata via YouTube Search API : {query}")
        try:
            response = self._youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=1
            ).execute()
            return [
                TrackMetadata(
                    url=f"https://www.youtube.com/watch?v={item["id"]["videoId"]}",
                    title=html.unescape(item["snippet"]["title"]),
                    source=html.unescape(item["snippet"]["channelTitle"]),
                    thumbnail=item["snippet"]["thumbnails"]["medium"]["url"]
                ) for item in response["items"]
            ]
        except googleapiclient.errors.HttpError as e:
            self._logger.warning(f"YouTube search API returned error : {repr(e)}")
            raise MetadataFetchingException(
                "I could not fetch the track, YouTube search API returned error status : {error}",
                error=f"`{e.status_code}` : `{e.reason}`"
            )