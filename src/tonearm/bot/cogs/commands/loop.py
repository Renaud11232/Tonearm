import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager
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
        description="Sets the loop mode of the current playback queue"
    )
    async def loop(self,
                   interaction: nextcord.Interaction,
                   mode: LoopModeConverter = SlashOption(choices=["off", "track", "queue"])):
        await self.__loop(interaction, mode)

    @nextcord.slash_command(
        description="Sets the loop mode of the current playback queue"
    )
    async def repeat(self,
                     interaction: nextcord.Interaction,
                     mode: LoopModeConverter = SlashOption(choices=["off", "track", "queue"])):
        await self.__loop(interaction, mode)

    async def __loop(self, interaction: nextcord.Interaction, mode: LoopMode):
        self.__logger.debug(f"Handling `loop` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).loop(interaction.user, mode)
        await interaction.followup.send(
            embed=self.__embed_service.loop(mode)
        )
        self.__logger.debug(f"Successfully handled `loop` command (interaction:{interaction.id})")
