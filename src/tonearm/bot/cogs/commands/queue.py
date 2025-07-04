import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import IsCorrectChannel
from tonearm.bot.cogs.converters import ZeroIndexConverter
from tonearm.bot.managers import PlayerManager, I18nManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class QueueCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_service: EmbedService,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.queue, checks=[
            application_checks.guild_only(),
            is_correct_channel()
        ])

    @nextcord.slash_command(
        name="queue",
        description=I18nManager.get(Locale.en_US).gettext("Show the current queue"),
        description_localizations={
            Locale.en_US: I18nManager.get(Locale.en_US).gettext("Show the current queue"),
            Locale.fr: I18nManager.get(Locale.fr).gettext("Show the current queue"),
        }
    )
    async def queue(self,
                    interaction: nextcord.Interaction,
                    page: ZeroIndexConverter = SlashOption(
                        name=I18nManager.get(Locale.en_US).gettext("page"),
                        name_localizations={
                            Locale.en_US: I18nManager.get(Locale.en_US).gettext("page"),
                            Locale.fr: I18nManager.get(Locale.fr).gettext("page")
                        },
                        description=I18nManager.get(Locale.en_US).gettext("Page to display"),
                        description_localizations={
                            Locale.en_US: I18nManager.get(Locale.en_US).gettext("Page to display"),
                            Locale.fr: I18nManager.get(Locale.fr).gettext("Page to display")
                        },
                        required=False,
                        default=0,
                        min_value=1
                    )):
        self.__logger.debug(f"Handling `queue` command (interaction:{interaction.id})")
        await interaction.response.defer()
        status = self.__player_manager.get(interaction.guild).queue(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.queue(status, page) # type: ignore
        )
        self.__logger.debug(f"Successfully handled `queue` command (interaction:{interaction.id}, with status : {repr(status)}")