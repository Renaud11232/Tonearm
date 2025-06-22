import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import IsCorrectChannel
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class HistoryCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_service: EmbedService,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.history, checks=[
            application_checks.guild_only(),
            is_correct_channel()
        ])

    @nextcord.slash_command(
        description="Show the previously played tracks"
    )
    async def history(self,
                      interaction: nextcord.Interaction,
                      page: int = SlashOption(required=False, default=1, min_value=1)):
        self.__logger.debug(f"Handling `history` command (interaction:{interaction.id})")
        await interaction.response.defer()
        previous_tracks = self.__player_manager.get(interaction.guild).history(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.history(previous_tracks, page)
        )
        self.__logger.debug(f"Successfully handled `history` command (interaction:{interaction.id}, with previous tracks : {repr(previous_tracks)}")