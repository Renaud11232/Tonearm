import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, application_checks

from injector import singleton, inject

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class BackCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Jumps back to a specific track in the history"
    )
    @application_checks.guild_only()
    async def back(self,
                   interaction: nextcord.Interaction,
                   track: int = SlashOption(required=True, min_value=1)):
        await self.__back(interaction, track)

    @nextcord.slash_command(
        description="Jumps back to a specific track in the history"
    )
    @application_checks.guild_only()
    async def unskipto(self,
                       interaction: nextcord.Interaction,
                       track: int = SlashOption(required=True, min_value=1)):
        await self.__back(interaction, track)

    async def __back(self, interaction: nextcord.Interaction, track: int):
        self.__logger.debug(f"Handling `back` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).back(interaction.user, track)
        await interaction.followup.send(
            embed=self.__embed_service.back(track)
        )
        self.__logger.debug(f"Successfully handled `back` command (interaction:{interaction.id})")