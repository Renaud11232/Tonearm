import logging

import nextcord
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class PauseCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Pauses the currently playing track"
    )
    async def pause(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `pause` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).pause(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.pause()
        )
        self.__logger.debug(f"Successfully handled `pause` command (interaction:{interaction.id}")