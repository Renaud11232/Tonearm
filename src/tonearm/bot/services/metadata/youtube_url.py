import re
from urllib.parse import urlparse, parse_qs
from typing import List
import html

from injector import singleton, inject

import googleapiclient.errors

from tonearm.configuration import Configuration

from .exceptions import MetadataFetchingException
from .base import YoutubeMetadataService
from .metadata import TrackMetadata


@singleton
class YoutubeUrlMetadataService(YoutubeMetadataService):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__(configuration)
        self.__configuration = configuration

    def fetch(self, query: str) -> List[TrackMetadata]:
        self._logger.debug(f"Fetching metadata via YouTube API : {query}")
        if self.__is_playlist(query):
            return self.__fetch_playlist(query)
        else:
            return self.__fetch_video(query)

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
            raise MetadataFetchingException(
                "I could not fetch the track, it looks like the URL you provided doesn't include a YouTube video ID."
            )
        return results.group(1)

    def __fetch_video(self, url: str) -> List[TrackMetadata]:
        id = self.__get_video_id(url)
        self._logger.debug(f"Fetching metadata via YouTube Videos API for video id : {id}")
        try:
            response = self._youtube.videos().list(
                part="snippet",
                id=id,
                maxResults=1
            ).execute()
            return [
                TrackMetadata(
                    url=url,
                    title=html.unescape(item["snippet"]["title"]),
                    source=html.unescape(item["snippet"]["channelTitle"]),
                    thumbnail=item["snippet"]["thumbnails"]["medium"]["url"]
                ) for item in response["items"]
            ]
        except googleapiclient.errors.HttpError as e:
            self._logger.warning(f"YouTube videos API returned error : {repr(e)}")
            raise MetadataFetchingException(
                "I could not fetch the track, YouTube videos API returned error status : {error}",
                error=f"{e.status_code}` : `{e.reason}`"
            )

    def __fetch_playlist(self, url: str) -> List[TrackMetadata]:
        id = self.__get_playlist_id(url)
        self._logger.debug(f"Fetching metadata via YouTube Playlist Items API for playlist id : {id}")
        try:
            items = []
            request = self._youtube.playlistItems().list(
                part="snippet",
                playlistId=id,
                maxResults=self.__configuration.max_playlist_length
            )
            while request:
                response = request.execute()
                for item in response["items"]:
                    if len(items) >= self.__configuration.max_playlist_length:
                        break
                    items.append(
                        TrackMetadata(
                            url=f"https://www.youtube.com/watch?v={item["snippet"]["resourceId"]["videoId"]}",
                            title=html.unescape(item["snippet"]["title"]),
                            source=html.unescape(item["snippet"]["videoOwnerChannelTitle"]),
                            thumbnail=item["snippet"]["thumbnails"]["medium"]["url"]
                        )
                    )
                if len(items) >= self.__configuration.max_playlist_length:
                    request = None
                else:
                    request = self._youtube.playlistItems().list_next(request, response)
            return items
        except googleapiclient.errors.HttpError as e:
            self._logger.warning(f"YouTube playlistItems API returned error : {repr(e)}")
            raise MetadataFetchingException(
                "I could not fetch the playlist, YouTube playlistItems API returned error status : {error}",
                error=f"`{e.status_code}` : `{e.reason}`"
            )
