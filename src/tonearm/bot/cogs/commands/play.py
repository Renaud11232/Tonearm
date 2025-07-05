import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class PlayCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.play, checks=[
            application_checks.guild_only(),
            is_correct_channel()
        ])

    @nextcord.slash_command(
        name="play",
        description=TranslationsManager().get(Locale.en_US).gettext("Play a track or playlist in your voice channel. You can provide link, or search for a track"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Play a track or playlist in your voice channel. You can provide link, or search for a track"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Play a track or playlist in your voice channel. You can provide link, or search for a track"),
        }
    )
    async def play(self,
                   interaction: nextcord.Interaction,
                   query: str = SlashOption(
                       name=TranslationsManager().get(Locale.en_US).gettext("query"),
                       name_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("query"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("query"),
                       },
                       description=TranslationsManager().get(Locale.en_US).gettext("Track or playlist to play. You can provide a link, or search for a track"),
                       description_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Track or playlist to play. You can provide a link, or search for a track"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("Track or playlist to play. You can provide a link, or search for a track"),
                       },
                       required=True
                   )):
        self.__logger.debug(f"Handling `play` command (interaction:{interaction.id})")
        await interaction.response.defer()
        tracks = await self.__player_manager.get(interaction.guild).play(interaction.user, query)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).play(tracks)
        )
        self.__logger.debug(f"Successfully handled `play` command (interaction:{interaction.id}), adding {len(tracks)} track(s) to the queue")