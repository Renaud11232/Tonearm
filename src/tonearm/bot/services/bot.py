import logging

from nextcord.ext import commands


class BotService:

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__logger = logging.getLogger("tonearm.services")

    async def shutdown(self):
        self.__logger.info("Shutdown requested. Goodbye !")
        await self.__bot.close()