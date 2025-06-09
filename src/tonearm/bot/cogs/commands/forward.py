import logging

import nextcord
from nextcord.ext import commands

from tonearm.bot.cogs.converters import Duration
from tonearm.bot.managers import ServiceManager
from tonearm.bot.exceptions import TonearmException


class ForwardCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Forwards a specific amount of time into the track"
    )
    async def forward(self, interaction: nextcord.Interaction, duration: Duration):
        self.__logger.debug(f"Handling forward command (interaction:{interaction.id})")
        await interaction.response.defer()
        player = self.__service_manager.get_player(interaction.guild)
        try:
            await player.forward(interaction.user, duration)
            await interaction.followup.send(f":fast_forward: Who needs intros anyway ?")
            self.__logger.debug(f"Successfully handled forward command (interaction:{interaction.id})")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")
            self.__logger.debug(f"Failed to handle forward command (interaction:{interaction.id}) due to exception ; {repr(e)}")