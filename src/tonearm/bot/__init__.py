import logging
import sys

from tonearm.bot.cogs import *
from tonearm.bot.managers import QueueManager

from nextcord.ext import commands


class Tonearm:

    def __init__(self, token: str, log_level: str):
        self.__token = token
        self.__log_level = log_level
        self.__bot = commands.Bot()
        self.__queue_manager = QueueManager(self.__bot)
        self.__init_commands()

    def __init_logger(self, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(self.__log_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)
        return logger

    def __init_commands(self):
        self.__bot.add_cog(ReadyListener(self.__bot, self.__init_logger("tonearm.ready")))
        self.__bot.add_cog(Clean(self.__bot))
        self.__bot.add_cog(Clear())
        self.__bot.add_cog(Dj())
        self.__bot.add_cog(Forward())
        self.__bot.add_cog(JoinCommand(self.__queue_manager))
        self.__bot.add_cog(Jump())
        self.__bot.add_cog(LeaveCommand(self.__queue_manager))
        self.__bot.add_cog(Loop())
        self.__bot.add_cog(Move())
        self.__bot.add_cog(Next())
        self.__bot.add_cog(Now())
        self.__bot.add_cog(Pause())
        self.__bot.add_cog(Play())
        self.__bot.add_cog(Previous())
        self.__bot.add_cog(Queue())
        self.__bot.add_cog(Remove())
        self.__bot.add_cog(Resume())
        self.__bot.add_cog(Rewind())
        self.__bot.add_cog(Seek())
        self.__bot.add_cog(Setting())
        self.__bot.add_cog(Shuffle())
        self.__bot.add_cog(Stop())
        self.__bot.add_cog(Voteskip())

    def run(self):
        self.__bot.run(self.__token)
