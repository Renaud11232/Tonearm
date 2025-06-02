import logging

from nextcord.ext import commands

from tonearm.bot.managers import ServiceManager


class ReadyListener(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.listeners")

    @commands.Cog.listener()
    async def on_ready(self):
        self.__logger.debug("Handling ready event")
        await self.__service_manager.get_bot().on_ready()
        self.__logger.debug("Successfully handled ready event")