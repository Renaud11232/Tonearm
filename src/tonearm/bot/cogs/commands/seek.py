import logging

import nextcord
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.cogs.converters import DurationConverter
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class SeekCommand(CommandCogBase):

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
        self._add_checks(self.seek, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        description="Seeks to a specific time in the track"
    )
    async def seek(self, interaction: nextcord.Interaction, duration: DurationConverter):
        self.__logger.debug(f"Handling `seek` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).seek(interaction.user, duration)
        await interaction.followup.send(
            embed=self.__embed_service.seek()
        )
        self.__logger.debug(f"Successfully handled `seek` command (interaction:{interaction.id})")