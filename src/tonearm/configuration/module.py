import argparse
import logging

from injector import Module, singleton, provider

from .configuration import Configuration
from .action import EnvDefault


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
            "--cobalt-api-url",
            action=EnvDefault,
            type=str,
            required=True,
            env_var="COBALT_API_URL",
            help="URL of the cobalt.tools instance to use to download media"
        )
        parser.add_argument(
            "--cobalt-api-key",
            action=EnvDefault,
            type=str,
            required=False,
            env_var="COBALT_API_KEY",
            help="API key used to authenticate on the configured cobalt.tools instance"
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
        args = parser.parse_args()
        return Configuration(
            discord_token=args.discord_token,
            log_level=args.log_level,
            youtube_api_key=args.youtube_api_key,
            cobalt_api_key=args.cobalt_api_key,
            cobalt_api_url=args.cobalt_api_url,
            data_path=args.data_path,
        )