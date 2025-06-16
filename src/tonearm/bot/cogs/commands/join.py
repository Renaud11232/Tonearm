import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class JoinCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Joins your current voice channel"
    )
    async def join(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling join command (interaction:{interaction.id})")
        await interaction.response.defer()
        player_service = await self.__player_manager.get(interaction.guild)
        await player_service.join(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.join()
        )
        self.__logger.debug(f"Successfully handled join command (interaction:{interaction.id})")