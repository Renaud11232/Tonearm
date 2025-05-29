import logging
import sys

from tonearm.bot.cogs import *
from tonearm.bot.managers import PlayerManager

from nextcord.ext import commands

from tonearm.bot.services.media import MediaService
from tonearm.bot.services.metadata import MetadataService


class Tonearm:

    def __init__(self, token: str, log_level: str, youtube_api_key: str | None, cobalt_api_url: str, cobalt_api_key: str | None):
        self.__token = token
        self.__log_level = log_level
        self.__init_logger("nextcord")
        self.__init_logger("tonearm")
        self.__bot = commands.Bot()
        self.__player_manager = PlayerManager(self.__bot, MetadataService(youtube_api_key), MediaService(cobalt_api_url, cobalt_api_key))
        self.__init_commands()

    def __init_logger(self, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(self.__log_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

    def __init_commands(self):
        self.__bot.add_cog(ReadyListener(self.__bot))
        self.__bot.add_cog(CleanCommand(self.__bot))
        self.__bot.add_cog(Clear())
        self.__bot.add_cog(Dj())
        self.__bot.add_cog(Forward())
        self.__bot.add_cog(JoinCommand(self.__player_manager))
        self.__bot.add_cog(Jump())
        self.__bot.add_cog(LeaveCommand(self.__bot, self.__player_manager))
        self.__bot.add_cog(Loop())
        self.__bot.add_cog(Move())
        self.__bot.add_cog(NextCommand(self.__player_manager))
        self.__bot.add_cog(Now())
        self.__bot.add_cog(Pause())
        self.__bot.add_cog(PlayCommand(self.__player_manager))
        self.__bot.add_cog(Previous())
        self.__bot.add_cog(Queue())
        self.__bot.add_cog(Remove())
        self.__bot.add_cog(Resume())
        self.__bot.add_cog(Rewind())
        self.__bot.add_cog(Seek())
        self.__bot.add_cog(Setting())
        self.__bot.add_cog(Shuffle())
        self.__bot.add_cog(Stop(self.__player_manager))
        self.__bot.add_cog(VersionCommand())
        self.__bot.add_cog(Voteskip())

    def run(self):
        self.__bot.run(self.__token)
