import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class StopCommand(CommandCogBase):

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
        self._add_checks(self.stop, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="stop",
        description=TranslationsManager().get(Locale.en_US).gettext("Stop the current playback"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Stop the current playback"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Stop the current playback"),
        }
    )
    async def stop(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `stop` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).stop(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).stop()
        )
        self.__logger.debug(f"Successfully handled `stop` command (interaction:{interaction.id})")