import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import IsCorrectChannel
from tonearm.bot.managers import TranslationsManager, EmbedManager
from tonearm.bot.services import BotService

from .base import CommandCogBase


@singleton
class VersionCommand(CommandCogBase):

    @inject
    def __init__(self,
                 bot_service: BotService,
                 embed_manager: EmbedManager,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__bot_service = bot_service
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.version, checks=[
            application_checks.guild_only(),
            is_correct_channel()
        ])

    @nextcord.slash_command(
        name="version",
        description=TranslationsManager().get(Locale.en_US).gettext("Show nerdy details about the bot"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Show nerdy details about the bot"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Show nerdy details about the bot"),
        }
    )
    async def version(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `version` command (interaction:{interaction.id})")
        await interaction.response.defer()
        version = self.__bot_service.version()
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).version(version)
        )
        self.__logger.debug(f"Successfully handled `version` command (interaction:{interaction.id}), returning {repr(version)}")