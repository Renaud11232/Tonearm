import threading

import nextcord
from nextcord.ext import commands

from tonearm.bot.services import PlayerService


class PlayerManager:

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__lock = threading.Lock()
        self.__players = {}

    def get_player(self, guild: nextcord.Guild) -> PlayerService:
        with self.__lock:
            if not guild.id in self.__players:
                self.__players[guild.id] = PlayerService(self.__bot)
            return self.__players[guild.id]