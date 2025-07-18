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
class RemoveCommand(CommandCogBase):

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
        self._add_checks(self.remove, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="remove",
        description=TranslationsManager().get(Locale.en_US).gettext("Remove a track from the queue"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Remove a track from the queue"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Remove a track from the queue"),
        }
    )
    async def remove(self,
                     interaction: nextcord.Interaction,
                     track: ZeroIndexConverter = SlashOption(
                         name=TranslationsManager().get(Locale.en_US).gettext("track"),
                         name_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("track"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("track")
                         },
                         description=TranslationsManager().get(Locale.en_US).gettext("Track number to remove"),
                         description_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Track number to remove"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("Track number to remove"),
                         },
                         required=True,
                         min_value=0
                     )):
        self.__logger.debug(f"Handling `remove` command (interaction:{interaction.id})")
        await interaction.response.defer()
        removed_track = await self.__player_manager.get(interaction.guild).remove(interaction.user, track) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).remove(removed_track)
        )
        self.__logger.debug(f"Successfully handled `remove` command (interaction:{interaction.id})")