import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import IsCorrectChannel, IsNotAnarchy
from tonearm.bot.managers import TranslationsManager, EmbedManager, PlayerManager

from .base import CommandCogBase


@singleton
class VotenextCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 is_correct_channel: IsCorrectChannel,
                 is_not_anarchy: IsNotAnarchy):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.votenext, self.voteskip, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            is_not_anarchy()
        ])

    @nextcord.slash_command(
        name="votenext",
        description=TranslationsManager().get(Locale.en_US).gettext("Vote to skip the current track"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Vote to skip the current track"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Vote to skip the current track"),
        }
    )
    async def votenext(self, interaction: nextcord.Interaction):
        await self.__votenext(interaction)

    @nextcord.slash_command(
        name="voteskip",
        description=TranslationsManager().get(Locale.en_US).gettext("Vote to skip the current track"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Vote to skip the current track"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Vote to skip the current track"),
        }
    )
    async def voteskip(self, interaction: nextcord.Interaction):
        await self.__votenext(interaction)

    async def __votenext(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `votenext` command (interaction:{interaction.id})")
        await interaction.response.defer()
        status = await self.__player_manager.get(interaction.guild).votenext(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).votenext(status)
        )
        self.__logger.debug(f"Successfully handled `votenext` command (interaction:{interaction.id})")
