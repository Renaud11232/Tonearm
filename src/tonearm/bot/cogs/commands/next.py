import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class NextCommand(CommandCogBase):

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
        self._add_checks(self.next, self.skip, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="next",
        description=TranslationsManager().get(Locale.en_US).gettext("Skip the current playing track to the next one"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Skip the current playing track to the next one"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Skip the current playing track to the next one")
        }
    )
    async def next(self, interaction: nextcord.Interaction):
        await self.__next(interaction)

    @nextcord.slash_command(
        name="skip",
        description=TranslationsManager().get(Locale.en_US).gettext("Skip the current playing track to the next one"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Skip the current playing track to the next one"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Skip the current playing track to the next one")
        }
    )
    async def skip(self, interaction: nextcord.Interaction):
        await self.__next(interaction)

    async def __next(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `next` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).jump(interaction.user, 0)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).next()
        )
        self.__logger.debug(f"Successfully handled `next` command (interaction:{interaction.id})")