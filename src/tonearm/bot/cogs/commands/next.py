import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager
from tonearm.bot.exceptions import TonearmException

class NextCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Skips the current playing track to the next one"
    )
    async def next(self, interaction: nextcord.Interaction):
        await self.__next(interaction)

    @nextcord.slash_command(
        description="Skips the current playing track to the next one"
    )
    async def skip(self, interaction: nextcord.Interaction):
        await self.__next(interaction)

    async def __next(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling next command (interaction:{interaction.id})")
        await interaction.response.defer()
        player = self.__service_manager.get_player(interaction.guild)
        try:
            await player.next(interaction.user)
            await interaction.followup.send(f":fast_forward: Skipping to the next track, I didn't like this one either")
            self.__logger.debug(f"Successfully handled next command (interaction:{interaction.id})")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")
            self.__logger.debug(f"Failed to handle next command (interaction:{interaction.id}) due to exception : {repr(e)}")