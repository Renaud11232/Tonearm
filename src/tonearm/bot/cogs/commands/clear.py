import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class ClearCommand(CommandCogBase):

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
        self._add_checks(self.clear, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="clear",
        description=TranslationsManager().get(Locale.en_US).gettext("Clear all songs in the queue"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Clear all songs in the queue"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Clear all songs in the queue"),
        }
    )
    async def clear(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `clear` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).clear(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).clear()
        )
        self.__logger.debug(f"Successfully handled `clear` command (interaction:{interaction.id})")