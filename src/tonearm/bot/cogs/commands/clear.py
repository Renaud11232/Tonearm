import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager
from tonearm.bot.exceptions import TonearmException

class ClearCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Clears all songs in the queue"
    )
    async def clear(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling clear command (interaction:{interaction.id})")
        await interaction.response.defer()
        player = self.__service_manager.get_player(interaction.guild)
        try:
            await player.clear(interaction.user)
            await interaction.followup.send(f":broom: Wiped the queue. Sometimes starting fresh hits different.")
            self.__logger.debug(f"Successfully handled clear command (interaction:{interaction.id})")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")
            self.__logger.debug(f"Failed to handle clear command (interaction:{interaction.id}) due to exception ; {repr(e)}")