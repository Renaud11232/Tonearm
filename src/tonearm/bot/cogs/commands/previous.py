import logging

import nextcord
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class PreviousCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Play the previous track from the queue"
    )
    async def previous(self, interaction: nextcord.Interaction):
        await self.__previous(interaction)

    @nextcord.slash_command(
        description="Play the previous track from the queue"
    )
    async def unskip(self, interaction: nextcord.Interaction):
        await self.__previous(interaction)

    async def __previous(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `previous` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).back(interaction.user, 1)
        await interaction.followup.send(
            embed=self.__embed_service.previous()
        )
        self.__logger.debug(f"Successfully handled `previous` command (interaction:{interaction.id})")