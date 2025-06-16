import logging

import nextcord
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class NowCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Shows the current playing track"
    )
    async def now(self, interaction: nextcord.Interaction):
        await self.__now(interaction)

    @nextcord.slash_command(
        name="now-playing",
        description="Shows the current playing track"
    )
    async def now_playing(self, interaction: nextcord.Interaction):
        await self.__now(interaction)

    async def __now(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling now command (interaction:{interaction.id})")
        await interaction.response.defer()
        player_service = await self.__player_manager.get(interaction.guild)
        status = await player_service.now(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.now(status)
        )
        self.__logger.debug(f"Successfully handled now command (interaction:{interaction.id}, with status : {repr(status)}")