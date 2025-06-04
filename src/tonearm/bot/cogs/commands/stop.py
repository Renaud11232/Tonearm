import logging

import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import ServiceManager
from tonearm.bot.exceptions import TonearmException

class StopCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Stops the current playback"
    )
    async def stop(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling stop command (interaction:{interaction.id})")
        await interaction.response.defer()
        player = self.__service_manager.get_player(interaction.guild)
        try:
            await player.stop(interaction.user)
            await interaction.followup.send(f":vertical_traffic_light: Stopped playback")
            self.__logger.debug(f"Successfully handled stop command (interaction:{interaction.id})")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")
            self.__logger.debug(f"Failed to handle stop command (interaction:{interaction.id}) due to exception : {repr(e)}")