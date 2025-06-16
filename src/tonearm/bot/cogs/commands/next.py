import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class NextCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
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
        player_service = await self.__player_manager.get(interaction.guild)
        await player_service.next(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.next()
        )
        self.__logger.debug(f"Successfully handled next command (interaction:{interaction.id})")