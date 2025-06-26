import logging

import nextcord
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class ShuffleCommand(CommandCogBase):

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
        self._add_checks(self.shuffle, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        name="shuffle",
        description="Shuffles tracks in the queue"
    )
    async def shuffle(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `shuffle` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).shuffle(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.shuffle()
        )
        self.__logger.debug(f"Successfully handled `shuffle` command (interaction:{interaction.id}")