import logging
import asyncio

import nextcord
from nextcord.ext import commands

from injector import inject, noninjectable


class ChatService:

    @inject
    @noninjectable("channel")
    def __init__(self, channel: nextcord.TextChannel, bot: commands.Bot):
        self.__channel = channel
        self.__bot = bot
        self.__lock = asyncio.Lock()
        self.__logger = logging.getLogger("tonearm.chat")

    async def clean(self):
        async with self.__lock:
            messages = []
            self.__logger.debug(f"Browsing messages in channel {self.__channel.id}")
            async for message in self.__channel.history():
                if message.author == self.__bot.user:
                    self.__logger.debug(f"Deleting message {message.id} from channel {self.__channel.id}")
                    messages.append(message)
                    await message.delete()
            return messages