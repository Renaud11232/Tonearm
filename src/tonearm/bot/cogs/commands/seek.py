import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.cogs.converters import DurationConverter
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class SeekCommand(CommandCogBase):

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
        self._add_checks(self.seek, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="seek",
        description=TranslationsManager().get(Locale.en_US).gettext("Seek to a specific time in the track"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Seek to a specific time in the track"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Seek to a specific time in the track"),
        }
    )
    async def seek(self,
                   interaction: nextcord.Interaction,
                   duration: DurationConverter = SlashOption(
                       name=TranslationsManager().get(Locale.en_US).gettext("duration"),
                       name_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("duration"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("duration"),
                       },
                       description=TranslationsManager().get(Locale.en_US).gettext("Where to seek in the track"),
                       description_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Where to seek in the track"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("Where to seek in the track"),
                       },
                       required=True
                   )):
        self.__logger.debug(f"Handling `seek` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).seek(interaction.user, duration) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).seek()
        )
        self.__logger.debug(f"Successfully handled `seek` command (interaction:{interaction.id})")