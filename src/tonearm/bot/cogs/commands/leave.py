import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager
from tonearm.bot.exceptions import TonearmException

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
        player = self.__service_manager.get_player(interaction.guild)
        try:
            await player.leave(interaction.user)
            await interaction.followup.send(f":wave: Goodbye !")
            self.__logger.debug(f"Successfully handled leave command (interaction:{interaction.id})")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")
            self.__logger.debug(f"Failed to handle leave command (interaction:{interaction.id}) due to exception : {repr(e)}")
