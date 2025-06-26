import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.cogs.converters import ZeroIndexConverter
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class BackCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_service: EmbedService,
                 can_use_dj_command: CanUseDjCommand,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.back, self.unskipto, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="back",
        description="Jumps back to a specific track in the history"
    )
    async def back(self,
                   interaction: nextcord.Interaction,
                   track: ZeroIndexConverter = SlashOption(
                       name="track",
                       description="Track number to jump back to",
                       required=True,
                       min_value=1
                   )):
        await self.__back(interaction, track) # type: ignore

    @nextcord.slash_command(
        name="unskipto",
        description="Jumps back to a specific track in the history"
    )
    async def unskipto(self,
                       interaction: nextcord.Interaction,
                       track: ZeroIndexConverter = SlashOption(
                           name="track",
                           description="Track number to jump back to",
                           required=True,
                           min_value=1
                       )):
        await self.__back(interaction, track) # type: ignore

    async def __back(self, interaction: nextcord.Interaction, track: int):
        self.__logger.debug(f"Handling `back` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).back(interaction.user, track)
        await interaction.followup.send(
            embed=self.__embed_service.back(track)
        )
        self.__logger.debug(f"Successfully handled `back` command (interaction:{interaction.id})")
