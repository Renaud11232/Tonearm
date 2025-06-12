import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class StopCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Stops the current playback"
    )
    async def stop(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling stop command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).stop(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.stop()
        )
        self.__logger.debug(f"Successfully handled stop command (interaction:{interaction.id})")