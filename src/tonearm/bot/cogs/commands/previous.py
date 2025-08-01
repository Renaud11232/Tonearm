import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class PreviousCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 is_correct_channel: IsCorrectChannel,
                 can_use_dj_command: CanUseDjCommand,):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.previous, self.unskip, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="previous",
        description=TranslationsManager().get(Locale.en_US).gettext("Play the previous track from the queue"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Play the previous track from the queue"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Play the previous track from the queue"),
        }
    )
    async def previous(self, interaction: nextcord.Interaction):
        await self.__previous(interaction)

    @nextcord.slash_command(
        name="unskip",
        description=TranslationsManager().get(Locale.en_US).gettext("Play the previous track from the queue"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Play the previous track from the queue"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Play the previous track from the queue"),
        }
    )
    async def unskip(self, interaction: nextcord.Interaction):
        await self.__previous(interaction)

    async def __previous(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `previous` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).back(interaction.user, 0)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).previous()
        )
        self.__logger.debug(f"Successfully handled `previous` command (interaction:{interaction.id})")