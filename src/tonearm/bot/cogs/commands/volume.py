import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class VolumeCommand(CommandCogBase):

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
        self._add_checks(self.volume, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])


    @nextcord.slash_command(
        name="volume",
        description=TranslationsManager().get(Locale.en_US).gettext("Change the volume of the playing tracks"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Change the volume of the playing tracks"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Change the volume of the playing tracks"),
        }
    )
    async def volume(self,
                     interaction: nextcord.Interaction,
                     value: int = SlashOption(
                         name=TranslationsManager().get(Locale.en_US).gettext("value"),
                         name_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("value"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("value"),
                         },
                         description=TranslationsManager().get(Locale.en_US).gettext("Playback volume (between 0 and 200)"),
                         description_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Playback volume (between 0 and 200)"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("Playback volume (between 0 and 200)"),
                         },
                         required=True,
                         min_value=0,
                         max_value=200
                     )):
        self.__logger.debug(f"Handling `volume` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).volume(interaction.user, value)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).volume(value)
        )
        self.__logger.debug(f"Successfully handled `volume` command (interaction:{interaction.id}, setting volume to : {repr(value)}")