import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.cogs.converters import ZeroIndexConverter
from tonearm.bot.managers import PlayerManager, I18nManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class MoveCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_service: EmbedService,
                 is_correct_channel: IsCorrectChannel,
                 can_use_dj_command: CanUseDjCommand):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.move, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="move",
        description=I18nManager.get(Locale.en_US).gettext("Move the position of a track in the queue"),
        description_localizations={
            Locale.en_US: I18nManager.get(Locale.en_US).gettext("Move the position of a track in the queue"),
            Locale.fr: I18nManager.get(Locale.fr).gettext("Move the position of a track in the queue")
        }
    )
    async def move(self,
                   interaction: nextcord.Interaction,
                   fr0m: ZeroIndexConverter = SlashOption(
                       name=I18nManager.get(Locale.en_US).gettext("from"),
                       name_localizations={
                           Locale.en_US: I18nManager.get(Locale.en_US).gettext("from"),
                           Locale.fr: I18nManager.get(Locale.en_US).gettext("from")
                       },
                       description=I18nManager.get(Locale.en_US).gettext("Initial track position"),
                       description_localizations={
                           Locale.en_US: I18nManager.get(Locale.en_US).gettext("Initial track position"),
                           Locale.fr: I18nManager.get(Locale.fr).gettext("Initial track position"),
                       },
                       required=True,
                       min_value=1
                   ),
                   to: ZeroIndexConverter = SlashOption(
                       name=I18nManager.get(Locale.en_US).gettext("to"),
                       name_localizations={
                           Locale.en_US: I18nManager.get(Locale.en_US).gettext("to"),
                           Locale.fr: I18nManager.get(Locale.en_US).gettext("to")
                       },
                       description=I18nManager.get(Locale.en_US).gettext("Target track position"),
                       description_localizations={
                           Locale.en_US: I18nManager.get(Locale.en_US).gettext("Target track position"),
                           Locale.fr: I18nManager.get(Locale.fr).gettext("Target track position"),
                       },
                       required=True,
                       min_value=1
                   )):
        self.__logger.debug(f"Handling `move` command (interaction:{interaction.id})")
        await interaction.response.defer()
        moved_track = await self.__player_manager.get(interaction.guild).move(interaction.user, fr0m, to) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_service.move(moved_track, fr0m, to) # type: ignore
        )
        self.__logger.debug(f"Successfully handled `move` command (interaction:{interaction.id})")