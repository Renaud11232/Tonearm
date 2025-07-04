import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.services import BotService, EmbedService
from tonearm.bot.managers import I18nManager

from .base import CommandCogBase


@singleton
class ShutdownCommand(CommandCogBase):

    @inject
    def __init__(self, bot_service: BotService, embed_service: EmbedService):
        super().__init__()
        self.__bot_service = bot_service
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.shutdown, checks=[
            application_checks.guild_only(),
            application_checks.is_owner()
        ])

    @nextcord.slash_command(
        name="shutdown",
        description=I18nManager.get(Locale.en_US).gettext("Shut the bot down"),
        description_localizations={
            Locale.en_US: I18nManager.get(Locale.en_US).gettext("Shut the bot down"),
            Locale.fr: I18nManager.get(Locale.fr).gettext("Shut the bot down"),
        }
    )
    async def shutdown(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `shutdown` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await interaction.followup.send(
            embed=self.__embed_service.shutdown()
        )
        await self.__bot_service.shutdown()