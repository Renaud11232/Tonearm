import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class PauseCommand(CommandCogBase):

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
        self._add_checks(self.pause, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="pause",
        description=TranslationsManager().get(Locale.en_US).gettext("Pause the currently playing track"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Pause the currently playing track"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Pause the currently playing track"),
        }
    )
    async def pause(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `pause` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).pause(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).pause()
        )
        self.__logger.debug(f"Successfully handled `pause` command (interaction:{interaction.id}")