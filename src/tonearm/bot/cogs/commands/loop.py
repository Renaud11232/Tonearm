import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, I18nManager
from tonearm.bot.services import EmbedService
from tonearm.bot.cogs.converters import LoopModeConverter
from tonearm.bot.services.player import LoopMode

from .base import CommandCogBase


@singleton
class LoopCommand(CommandCogBase):

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
        self._add_checks(self.loop, self.repeat, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="loop",
        description=I18nManager.get(Locale.en_US).gettext("Set the loop mode of the current playback queue"),
        description_localizations={
            Locale.en_US: I18nManager.get(Locale.en_US).gettext("Set the loop mode of the current playback queue"),
            Locale.fr: I18nManager.get(Locale.fr).gettext("Set the loop mode of the current playback queue"),
        }
    )
    async def loop(self,
                   interaction: nextcord.Interaction,
                   mode: LoopModeConverter = SlashOption(
                       name=I18nManager.get(Locale.en_US).gettext("mode"),
                       name_localizations={
                           Locale.en_US: I18nManager.get(Locale.en_US).gettext("mode"),
                           Locale.fr: I18nManager.get(Locale.fr).gettext("mode"),
                       },
                       description=I18nManager.get(Locale.en_US).gettext("Loop mode to use"),
                       description_localizations={
                           Locale.en_US: I18nManager.get(Locale.en_US).gettext("Loop mode to use"),
                           Locale.fr: I18nManager.get(Locale.fr).gettext("Loop mode to use"),
                       },
                       choices={
                           I18nManager.get(Locale.en_US).gettext("off"): "off",
                           I18nManager.get(Locale.en_US).gettext("track"): "track",
                           I18nManager.get(Locale.en_US).gettext("queue"): "queue",
                       },
                       choice_localizations={
                           I18nManager.get(Locale.en_US).gettext("off"): {
                               Locale.en_US: I18nManager.get(Locale.en_US).gettext("off"),
                               Locale.fr: I18nManager.get(Locale.fr).gettext("off")
                           },
                           I18nManager.get(Locale.en_US).gettext("track"): {
                               Locale.en_US: I18nManager.get(Locale.en_US).gettext("track"),
                               Locale.fr: I18nManager.get(Locale.fr).gettext("track")
                           },
                           I18nManager.get(Locale.en_US).gettext("queue"): {
                               Locale.en_US: I18nManager.get(Locale.en_US).gettext("queue"),
                               Locale.fr: I18nManager.get(Locale.fr).gettext("queue")
                           }
                       },
                       required=True
                   )):
        await self.__loop(interaction, mode)  # type: ignore

    @nextcord.slash_command(
        name="repeat",
        description=I18nManager.get(Locale.en_US).gettext("Set the loop mode of the current playback queue"),
        description_localizations={
            Locale.en_US: I18nManager.get(Locale.en_US).gettext("Set the loop mode of the current playback queue"),
            Locale.fr: I18nManager.get(Locale.fr).gettext("Set the loop mode of the current playback queue"),
        }
    )
    async def repeat(self,
                     interaction: nextcord.Interaction,
                     mode: LoopModeConverter = SlashOption(
                         name=I18nManager.get(Locale.en_US).gettext("mode"),
                         name_localizations={
                             Locale.en_US: I18nManager.get(Locale.en_US).gettext("mode"),
                             Locale.fr: I18nManager.get(Locale.fr).gettext("mode"),
                         },
                         description=I18nManager.get(Locale.en_US).gettext("Loop mode to use"),
                         description_localizations={
                             Locale.en_US: I18nManager.get(Locale.en_US).gettext("Loop mode to use"),
                             Locale.fr: I18nManager.get(Locale.fr).gettext("Loop mode to use"),
                         },
                         choices={
                             I18nManager.get(Locale.en_US).gettext("off"): "off",
                             I18nManager.get(Locale.en_US).gettext("track"): "track",
                             I18nManager.get(Locale.en_US).gettext("queue"): "queue",
                         },
                         choice_localizations={
                             I18nManager.get(Locale.en_US).gettext("off"): {
                                 Locale.en_US: I18nManager.get(Locale.en_US).gettext("off"),
                                 Locale.fr: I18nManager.get(Locale.fr).gettext("off")
                             },
                             I18nManager.get(Locale.en_US).gettext("track"): {
                                 Locale.en_US: I18nManager.get(Locale.en_US).gettext("track"),
                                 Locale.fr: I18nManager.get(Locale.fr).gettext("track")
                             },
                             I18nManager.get(Locale.en_US).gettext("queue"): {
                                 Locale.en_US: I18nManager.get(Locale.en_US).gettext("queue"),
                                 Locale.fr: I18nManager.get(Locale.fr).gettext("queue")
                             }
                         },
                         required=True
                     )):
        await self.__loop(interaction, mode)  # type: ignore

    async def __loop(self, interaction: nextcord.Interaction, mode: LoopMode):
        self.__logger.debug(f"Handling `loop` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).loop(interaction.user, mode)
        await interaction.followup.send(
            embed=self.__embed_service.loop(mode)
        )
        self.__logger.debug(f"Successfully handled `loop` command (interaction:{interaction.id})")
