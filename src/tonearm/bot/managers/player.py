import threading

import nextcord
from nextcord.ext import commands

from tonearm.bot.services import PlayerService, MetadataService


class PlayerManager:

    def __init__(self, bot: commands.Bot, metadata_service: MetadataService):
        self.__bot = bot
        self.__metadata_service = metadata_service
        self.__lock = threading.Lock()
        self.__players = {}

    def get_player(self, guild: nextcord.Guild) -> PlayerService:
        with self.__lock:
            if not guild.id in self.__players:
                self.__players[guild.id] = PlayerService(self.__bot, self.__metadata_service)
            return self.__players[guild.id]