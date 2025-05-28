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
    args = parser.parse_args()
    tonearm = Tonearm(args.discord_token, args.log_level)
    tonearm.run()


if __name__ == "__main__":
    main()
