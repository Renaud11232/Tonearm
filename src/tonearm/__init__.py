import argparse
import logging

from tonearm.bot import Tonearm
from tonearm.cli.action import EnvDefault


def main():
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
        required=False,
        default=None,
        env_var="YOUTUBE_API_KEY",
        help="YouTube API key used to fetch video metadata. If omitted, YouTube support will be disabled"
    )
    args = parser.parse_args()
    tonearm = Tonearm(
        token=args.discord_token,
        log_level=args.log_level,
        youtube_api_key=args.youtube_api_key
    )
    tonearm.run()


if __name__ == "__main__":
    main()
