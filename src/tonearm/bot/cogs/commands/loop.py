import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager
from tonearm.bot.cogs.converters import LoopModeConverter
from tonearm.bot.services.player import LoopMode

from .base import CommandCogBase


@singleton
class LoopCommand(CommandCogBase):

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
        self._add_checks(self.loop, self.repeat, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="loop",
        description=TranslationsManager().get(Locale.en_US).gettext("Set the loop mode of the current playback queue"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Set the loop mode of the current playback queue"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Set the loop mode of the current playback queue"),
        }
    )
    async def loop(self,
                   interaction: nextcord.Interaction,
                   mode: LoopModeConverter = SlashOption(
                       name=TranslationsManager().get(Locale.en_US).gettext("mode"),
                       name_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("mode"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("mode"),
                       },
                       description=TranslationsManager().get(Locale.en_US).gettext("Loop mode to use"),
                       description_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Loop mode to use"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("Loop mode to use"),
                       },
                       choices=LoopModeConverter.get_choices(),
                       choice_localizations=LoopModeConverter.get_choice_localizations(),
                       required=True
                   )):
        await self.__loop(interaction, mode)  # type: ignore

    @nextcord.slash_command(
        name="repeat",
        description=TranslationsManager().get(Locale.en_US).gettext("Set the loop mode of the current playback queue"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Set the loop mode of the current playback queue"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Set the loop mode of the current playback queue"),
        }
    )
    async def repeat(self,
                     interaction: nextcord.Interaction,
                     mode: LoopModeConverter = SlashOption(
                         name=TranslationsManager().get(Locale.en_US).gettext("mode"),
                         name_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("mode"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("mode"),
                         },
                         description=TranslationsManager().get(Locale.en_US).gettext("Loop mode to use"),
                         description_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Loop mode to use"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("Loop mode to use"),
                         },
                         choices=LoopModeConverter.get_choices(),
                         choice_localizations=LoopModeConverter.get_choice_localizations(),
                         required=True
                     )):
        await self.__loop(interaction, mode)  # type: ignore

    async def __loop(self, interaction: nextcord.Interaction, mode: LoopMode):
        self.__logger.debug(f"Handling `loop` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).loop(interaction.user, mode)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).loop(mode)
        )
        self.__logger.debug(f"Successfully handled `loop` command (interaction:{interaction.id})")
