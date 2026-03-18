import logging
import sys

from injector import inject, singleton

from discord.ext import commands

from tonearm.configuration import Configuration


@singleton
class Tonearm:

    @inject
    def __init__(self, configuration: Configuration, bot: commands.Bot):
        self.__configuration = configuration
        self.__bot = bot

    def run(self):
        self.__bot.run(
            self.__configuration.discord_token,
            log_handler=logging.StreamHandler(sys.stdout),
            log_level=self.__configuration.log_level,
            root_logger=True
        )
