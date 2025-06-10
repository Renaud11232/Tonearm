import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager

class LeaveCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Leaves the current voice channel"
    )
    async def leave(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling leave command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__service_manager.get_player(interaction.guild).leave(interaction.user)
        await interaction.followup.send(f":microphone: Mic dropped. I'm gone.")
        self.__logger.debug(f"Successfully handled leave command (interaction:{interaction.id})")
