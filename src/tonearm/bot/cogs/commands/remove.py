import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.cogs.converters import ZeroIndexConverter
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class RemoveCommand(CommandCogBase):

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
        self._add_checks(self.remove, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])

    @nextcord.slash_command(
        description="Removes a track from the queue"
    )
    async def remove(self,
                     interaction: nextcord.Interaction,
                     track: ZeroIndexConverter = SlashOption(required=True, min_value=0)):
        self.__logger.debug(f"Handling `remove` command (interaction:{interaction.id})")
        await interaction.response.defer()
        removed_track = await self.__player_manager.get(interaction.guild).remove(interaction.user, track) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_service.remove(removed_track)
        )
        self.__logger.debug(f"Successfully handled `remove` command (interaction:{interaction.id})")