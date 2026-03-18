import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class ResumeCommand(CogBase):

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
        name="resume",
        description=app_commands.locale_str("Resume the currently paused track"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def resume(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `resume` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).resume(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).resume()
        )
        self.__logger.debug(f"Successfully handled `resume` command (interaction:{interaction.id}")