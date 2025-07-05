import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class LeaveCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 is_correct_channel: IsCorrectChannel,
                 can_use_dj_command: CanUseDjCommand):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.leave, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="leave",
        description=TranslationsManager().get(Locale.en_US).gettext("Leave the current voice channel"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Leave the current voice channel"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Leave the current voice channel")
        }
    )
    async def leave(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `leave` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).leave(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).leave()
        )
        self.__logger.debug(f"Successfully handled `leave` command (interaction:{interaction.id})")
