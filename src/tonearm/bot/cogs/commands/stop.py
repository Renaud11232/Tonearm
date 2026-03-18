import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class StopCommand(CogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 injector: Injector):
        super().__init__(injector)
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @app_commands.command(
        name="stop",
        description="Stop the current playback"
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def stop(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `stop` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).stop(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).stop()
        )
        self.__logger.debug(f"Successfully handled `stop` command (interaction:{interaction.id})")