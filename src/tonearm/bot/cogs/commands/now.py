import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import IsCorrectChannel
from tonearm.bot.managers import PlayerManager, I18nManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class NowCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_service: EmbedService,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.now, self.now_playing, checks=[
            application_checks.guild_only(),
            is_correct_channel()
        ])

    @nextcord.slash_command(
        name="now",
        description=I18nManager.get(Locale.en_US).gettext("Show the current playing track"),
        description_localizations={
            Locale.en_US: I18nManager.get(Locale.en_US).gettext("Show the current playing track"),
            Locale.fr: I18nManager.get(Locale.fr).gettext("Show the current playing track"),
        }
    )
    async def now(self, interaction: nextcord.Interaction):
        await self.__now(interaction)

    @nextcord.slash_command(
        name="now-playing",
        description=I18nManager.get(Locale.en_US).gettext("Show the current playing track"),
        description_localizations={
            Locale.en_US: I18nManager.get(Locale.en_US).gettext("Show the current playing track"),
            Locale.fr: I18nManager.get(Locale.fr).gettext("Show the current playing track"),
        }
    )
    async def now_playing(self, interaction: nextcord.Interaction):
        await self.__now(interaction)

    async def __now(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `now` command (interaction:{interaction.id})")
        await interaction.response.defer()
        status = self.__player_manager.get(interaction.guild).now(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.now(status)
        )
        self.__logger.debug(f"Successfully handled `now` command (interaction:{interaction.id}, with status : {repr(status)}")