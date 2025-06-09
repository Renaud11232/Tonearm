import logging

import nextcord
from nextcord.ext import commands, application_checks

from tonearm.bot.managers import ServiceManager


class ShutdownCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Shuts the bot down"
    )
    @application_checks.is_owner()
    async def shutdown(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling shutdown command (interaction:{interaction.id})")
        await interaction.send(":saluting_face: Initiating shutdown sequence... it’s been an honor.")
        await self.__service_manager.get_bot().shutdown()