import logging

import nextcord
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.cogs.converters import DurationConverter
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class ForwardCommand(CommandCogBase):

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
        self._add_checks(self.forward, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        description="Forwards a specific amount of time into the track"
    )
    async def forward(self, interaction: nextcord.Interaction, duration: DurationConverter):
        self.__logger.debug(f"Handling `forward` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).forward(interaction.user, duration) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_service.forward()
        )
        self.__logger.debug(f"Successfully handled `forward` command (interaction:{interaction.id})")