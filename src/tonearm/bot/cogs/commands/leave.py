import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class LeaveCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Leaves the current voice channel"
    )
    async def leave(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `leave` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).leave(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.leave()
        )
        self.__logger.debug(f"Successfully handled `leave` command (interaction:{interaction.id})")
