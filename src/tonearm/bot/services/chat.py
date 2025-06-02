import logging
import asyncio

import nextcord
from nextcord.ext import commands


class ChatService:

    def __init__(self, channel: nextcord.TextChannel, bot: commands.Bot):
        self.__channel = channel
        self.__bot = bot
        self.__lock = asyncio.Lock()
        self.__logger = logging.getLogger("tonearm.chat")

    async def clean(self):
        async with self.__lock:
            messages = []
            async for message in self.__channel.history():
                if message.author == self.__bot.user:
                    self.__logger.debug(f"Deleting message {message.id} from channel {message.channel.id}")
                    messages.append(message)
                    await message.delete()
            return messages