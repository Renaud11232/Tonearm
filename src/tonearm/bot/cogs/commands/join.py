import logging

import nextcord
from nextcord import Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import IsCorrectChannel
from tonearm.bot.managers import PlayerManager, TranslationsManager, EmbedManager

from .base import CommandCogBase


@singleton
class JoinCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.join, checks=[
            application_checks.guild_only(),
            is_correct_channel()
        ])


    @nextcord.slash_command(
        name="join",
        description=TranslationsManager().get(Locale.en_US).gettext("Join your current voice channel"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Join your current voice channel"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Join your current voice channel")
        }
    )
    async def join(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `join` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).join(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).join()
        )
        self.__logger.debug(f"Successfully handled `join` command (interaction:{interaction.id})")