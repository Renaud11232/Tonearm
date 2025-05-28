import threading

import nextcord
from nextcord.ext import commands

from tonearm.bot.services import QueueService


class QueueManager:

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__lock = threading.Lock()
        self.__queues = {}

    def get_queue(self, guild: nextcord.Guild) -> QueueService:
        with self.__lock:
            if not guild.id in self.__queues:
                self.__queues[guild.id] = QueueService(self.__bot)
            return self.__queues[guild.id]