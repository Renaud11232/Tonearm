import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.cogs.converters import ZeroIndexConverter
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class BackCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 can_use_dj_command: CanUseDjCommand,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.back, self.unskipto, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="back",
        description=TranslationsManager().get(Locale.en_US).gettext("Jump back to a specific track in the history"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Jump back to a specific track in the history"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Jump back to a specific track in the history")
        }
    )
    async def back(self,
                   interaction: nextcord.Interaction,
                   track: ZeroIndexConverter = SlashOption(
                       name=TranslationsManager().get(Locale.en_US).gettext("track"),
                       name_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("track"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("track")
                       },
                       description=TranslationsManager().get(Locale.en_US).gettext("Track number to jump back to"),
                       description_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Track number to jump back to"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("Track number to jump back to")
                       },
                       required=True,
                       min_value=1
                   )):
        await self.__back(interaction, track)  # type: ignore

    @nextcord.slash_command(
        name="unskipto",
        description=TranslationsManager().get(Locale.en_US).gettext("Jump back to a specific track in the history"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Jump back to a specific track in the history"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Jump back to a specific track in the history")
        }
    )
    async def unskipto(self,
                       interaction: nextcord.Interaction,
                       track: ZeroIndexConverter = SlashOption(
                           name=TranslationsManager().get(Locale.en_US).gettext("track"),
                           name_localizations={
                               Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("track"),
                               Locale.fr: TranslationsManager().get(Locale.fr).gettext("track")
                           },
                           description=TranslationsManager().get(Locale.en_US).gettext("Track number to jump back to"),
                           description_localizations={
                               Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Track number to jump back to"),
                               Locale.fr: TranslationsManager().get(Locale.fr).gettext("Track number to jump back to")
                           },
                           required=True,
                           min_value=1
                       )):
        await self.__back(interaction, track)  # type: ignore

    async def __back(self, interaction: nextcord.Interaction, track: int):
        self.__logger.debug(f"Handling `back` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).back(interaction.user, track)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).back(track)
        )
        self.__logger.debug(f"Successfully handled `back` command (interaction:{interaction.id})")
