import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager
from tonearm.bot.exceptions import TonearmException


class JoinCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Joins your current voice channel"
    )
    async def join(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling join command (interaction:{interaction.id})")
        await interaction.response.defer()
        player = self.__service_manager.get_player(interaction.guild)
        try:
            await player.join(interaction.user)
            await interaction.followup.send(f":notes: Let's get this party started !")
            self.__logger.debug(f"Successfully handled join command (interaction:{interaction.id})")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")
            self.__logger.debug(f"Failed to handle join command (interaction:{interaction.id}) due to exception : {repr(e)}")