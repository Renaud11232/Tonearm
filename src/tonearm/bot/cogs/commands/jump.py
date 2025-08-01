import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.cogs.converters import ZeroIndexConverter
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class JumpCommand(CommandCogBase):

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
        self._add_checks(self.jump, self.skipto, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="jump",
        description=TranslationsManager().get(Locale.en_US).gettext("Jump to a specific track in the queue"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Jump to a specific track in the queue"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Jump to a specific track in the queue")
        }
    )
    async def jump(self,
                   interaction: nextcord.Interaction,
                   track: ZeroIndexConverter = SlashOption(
                       name=TranslationsManager().get(Locale.en_US).gettext("track"),
                       name_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("track"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("track")
                       },
                       description=TranslationsManager().get(Locale.en_US).gettext("Track number to jump to"),
                       description_localizations={
                           Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Track number to jump to"),
                           Locale.fr: TranslationsManager().get(Locale.fr).gettext("Track number to jump to")
                       },
                       required=False,
                       min_value=1
                   )):
        await self.__jump(interaction, track) # type: ignore

    @nextcord.slash_command(
        name="skipto",
        description=TranslationsManager().get(Locale.en_US).gettext("Jump to a specific track in the queue"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Jump to a specific track in the queue"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Jump to a specific track in the queue")
        }
    )
    async def skipto(self,
                     interaction: nextcord.Interaction,
                     track: ZeroIndexConverter = SlashOption(
                         name=TranslationsManager().get(Locale.en_US).gettext("track"),
                         name_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("track"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("track")
                         },
                         description=TranslationsManager().get(Locale.en_US).gettext("Track number to jump to"),
                         description_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Track number to jump to"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("Track number to jump to")
                         },
                         required=False,
                         min_value=1
                     )):
        await self.__jump(interaction, track) # type: ignore

    async def __jump(self, interaction: nextcord.Interaction, track: int):
        self.__logger.debug(f"Handling `jump` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).jump(interaction.user, track)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).jump(track)
        )
        self.__logger.debug(f"Successfully handled `jump` command (interaction:{interaction.id})")