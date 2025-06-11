from typing import Any

import requests

from .exceptions import CobaltException


class CobaltClient:

    def __init__(self, base_url: str, api_key: str | None):
        self.__base_url = base_url
        self.__api_key = api_key

    def instance_info(self):
        return requests.get(self.__base_url).json()

    def process(self, url: str, *, audio_bitrate: str | None = None, audio_format: str | None = None,
                download_mode: str | None = None, filename_style: str | None = None, video_quality: str | None = None,
                disable_metadata: bool | None = None, always_proxy: bool | None = None,
                local_processing: bool | None = None, youtube_video_codec: str | None = None,
                youtube_dub_lang: str | None = None, convert_gif: bool | None = None, allow_h265: bool | None = None,
                tiktok_full_audio: bool | None = None, youtube_better_audio: bool | None = None,
                youtube_hls: bool | None = None):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if self.__api_key:
            headers["Authorization"] = f"Api-Key {self.__api_key}"
        data: dict[str, Any] = {
            "url": url
        }
        if audio_bitrate is not None:
            data["audioBitrate"] = audio_bitrate
        if audio_format is not None:
            data["audioFormat"] = audio_format
        if download_mode is not None:
            data["downloadMode"] = download_mode
        if filename_style is not None:
            data["filenameStyle"] = filename_style
        if video_quality is not None:
            data["videoQuality"] = video_quality
        if disable_metadata is not None:
            data["disableMetadata"] = disable_metadata
        if always_proxy is not None:
            data["alwaysProxy"] = always_proxy
        if local_processing is not None:
            data["localProcessing"] = local_processing
        if youtube_video_codec is not None:
            data["youtubeVideoCodec"] = youtube_video_codec
        if youtube_dub_lang is not None:
            data["youtubeDubLang"] = youtube_dub_lang
        if convert_gif is not None:
            data["convertGif"] = convert_gif
        if allow_h265 is not None:
            data["allowH265"] = allow_h265
        if tiktok_full_audio is not None:
            data["tiktokFullAudio"] = tiktok_full_audio
        if youtube_better_audio is not None:
            data["youtubeBetterAudio"] = youtube_better_audio
        if youtube_hls is not None:
            data["youtubeHLS"] = youtube_hls
        response =  requests.post(
            self.__base_url,
            json=data,
            headers=headers
        ).json()
        if response["status"] == "error":
            raise CobaltException(response["error"]["code"])
        return response