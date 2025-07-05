import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import IsCorrectChannel
from tonearm.bot.cogs.converters import ZeroIndexConverter
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class HistoryCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.history, checks=[
            application_checks.guild_only(),
            is_correct_channel()
        ])

    @nextcord.slash_command(
        name="history",
        description=TranslationsManager().get(Locale.en_US).gettext("Show the previously played tracks"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Show the previously played tracks"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Show the previously played tracks")
        }
    )
    async def history(self,
                      interaction: nextcord.Interaction,
                      page: ZeroIndexConverter = SlashOption(
                          name=TranslationsManager().get(Locale.en_US).gettext("page"),
                          name_localizations={
                              Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("page"),
                              Locale.fr: TranslationsManager().get(Locale.fr).gettext("page")
                          },
                          description=TranslationsManager().get(Locale.en_US).gettext("Page to display"),
                          description_localizations={
                              Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Page to display"),
                              Locale.fr: TranslationsManager().get(Locale.fr).gettext("Page to display")
                          },
                          required=False,
                          default=0,
                          min_value=1
                      )):
        self.__logger.debug(f"Handling `history` command (interaction:{interaction.id})")
        await interaction.response.defer()
        previous_tracks = self.__player_manager.get(interaction.guild).history(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).history(previous_tracks, page) # type: ignore
        )
        self.__logger.debug(f"Successfully handled `history` command (interaction:{interaction.id}, with previous tracks : {repr(previous_tracks)}")