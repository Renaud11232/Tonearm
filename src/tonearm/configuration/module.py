import argparse
import logging

import nextcord
from injector import Module, singleton, provider

from .configuration import Configuration
from .action import EnvDefault
from .converters import color


class ConfigurationModule(Module):

    @singleton
    @provider
    def provide_configuration(self) -> Configuration:
        parser = argparse.ArgumentParser(
            description="Starts a new Tonearm instance"
        )
        parser.add_argument(
            "--discord-token",
            action=EnvDefault,
            type=str,
            required=True,
            env_var="DISCORD_TOKEN",
            help="Bot token used to access Discord API. If omitted, the value of the `DISCORD_TOKEN` environment variable will be used."
        )
        parser.add_argument(
            "--log-level",
            action=EnvDefault,
            type=str,
            required=True,
            default="INFO",
            env_var="LOG_LEVEL",
            choices=logging.getLevelNamesMapping().keys(),
            help="Log level. If omitted, the value of the `LOG_LEVEL` environment variable will be used. Defaults to `INFO`"
        )
        parser.add_argument(
            "--youtube-api-key",
            action=EnvDefault,
            type=str,
            required=True,
            env_var="YOUTUBE_API_KEY",
            help="YouTube API key used to fetch video metadata. If omitted, YouTube support will be disabled"
        )
        parser.add_argument(
            "--max-playlist-length",
            action=EnvDefault,
            type=int,
            required=True,
            default=200,
            env_var="MAX_PLAYLIST_LENGTH",
            help="Maximum playlist length that can be added. Defaults to 200."
        )
        parser.add_argument(
            "--ffmpeg-executable",
            action=EnvDefault,
            type=str,
            required=True,
            default="ffmpeg",
            env_var="FFMPEG_EXECUTABLE",
            help="ffmpeg executable. This can also be a full path to the executable file"
        )
        parser.add_argument(
            "--youtube-cookies",
            action=EnvDefault,
            type=str,
            required=False,
            env_var="YOUTUBE_COOKIES",
            help="Path to the YouTube cookies file to use to avoid content restrictions or bot detection"
        )
        parser.add_argument(
            "--data-path",
            action=EnvDefault,
            type=str,
            required=True,
            default=".",
            env_var="DATA_PATH",
            help="Directory path where Tonearm will store its data and configuration. If omitted, the value of the `DATA_PATH` environment variable will be used. Defaults to the current working directory"
        )
        parser.add_argument(
            "--buffer-length",
            action=EnvDefault,
            type=int,
            required=True,
            default=60 * 60 * 2,
            env_var="BUFFER_LENGTH",
            help="Buffer length in seconds. This will be used to control how much memory will be used by players, as a tradeoff, setting smaller buffer sizes means you won't be able to seek far into long tracks. Defaults to 7200 seconds (2 hours)."
        )
        parser.add_argument(
            "--embed-color",
            action=EnvDefault,
            type=color,
            required=True,
            default="#71368A",
            env_var="EMBED_COLOR",
            help="Embed color. Defaults to #71368A (dark purple)"
        )
        parser.add_argument(
            "--status",
            action=EnvDefault,
            type=str,
            required=True,
            default=nextcord.Status.online.name,
            env_var="STATUS",
            choices=[s.name for s in nextcord.Status],
            help="Bot status. Defaults to `online`"
        )
        parser.add_argument(
            "--activity-type",
            action=EnvDefault,
            type=str,
            required=True,
            default=nextcord.ActivityType.listening.name,
            env_var="ACTIVITY_TYPE",
            choices=[t.name for t in nextcord.ActivityType if t.value >= 0],
            help="Bot activity type. Defaults to `listening`"
        )
        parser.add_argument(
            "--activity-name",
            action=EnvDefault,
            type=str,
            required=True,
            default="/play",
            env_var="ACTIVITY_NAME",
            help="Bot activity name. Defaults to `/play`"
        )
        parser.add_argument(
            "--activity-state",
            action=EnvDefault,
            type=str,
            required=False,
            env_var="ACTIVITY_STATE",
            help="Bot activity state, if the activity type is custom"
        )
        parser.add_argument(
            "--activity-url",
            action=EnvDefault,
            type=str,
            required=False,
            env_var="ACTIVITY_URL",
            help="Bot stream url, if the activity type is streaming."
        )
        args = parser.parse_args()
        return Configuration(
            discord_token=args.discord_token,
            log_level=args.log_level,
            youtube_api_key=args.youtube_api_key,
            max_playlist_length=args.max_playlist_length,
            ffmpeg_executable=args.ffmpeg_executable,
            youtube_cookies=args.youtube_cookies,
            data_path=args.data_path,
            buffer_length=args.buffer_length,
            colour=args.embed_color,
            status=nextcord.Status[args.status],  # type: ignore
            activity_type=nextcord.ActivityType[args.activity_type],
            activity_name=args.activity_name,
            activity_state=args.activity_state,
            activity_url=args.activity_url,
        )