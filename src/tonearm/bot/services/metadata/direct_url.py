from urllib.parse import urlparse, unquote_plus
from pathlib import PurePosixPath

import requests

import werkzeug.http

from typing import List

from injector import singleton

from .exceptions import MetadataFetchingException
from .base import MetadataServiceBase
from .metadata import TrackMetadata


@singleton
class DirectUrlMetadataService(MetadataServiceBase):

    def __init__(self):
        super().__init__()

    def fetch(self, query: str) -> List[TrackMetadata]:
        self._logger.debug(f"Fetching metadata for direct url : {query}")
        headers = {
            "Range": "bytes=0-0"
        }
        with requests.get(query, headers=headers, stream=True) as response:
            content_type = response.headers.get("Content-Type")
            if content_type is None or not content_type.startswith("audio/"):
                raise MetadataFetchingException(
                    "I could not fetch the track, the provided URL does not point to an audio file."
                )
            filename, domain = self.__parse_info(query, response.headers)
            return [
                TrackMetadata(
                    url=query,
                    title=filename,
                    source=domain,
                    thumbnail=None
                )
            ]

    @staticmethod
    def __parse_info(url, headers):
        parsed_url = urlparse(url)
        content_disposition = headers.get("Content-Disposition")
        if content_disposition is not None:
            param, options = werkzeug.http.parse_options_header(content_disposition)
            if param == "attachment":
                filename = options.get("filename")
                if filename is not None:
                    return filename, parsed_url.netloc
        path = PurePosixPath(parsed_url.path)
        return unquote_plus(path.name), parsed_url.netloc

