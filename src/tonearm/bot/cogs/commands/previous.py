import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class PreviousCommand(CogBase):

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
        name="previous",
        description=app_commands.locale_str("Play the previous track from the queue"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def previous(self, interaction: discord.Interaction):
        await self.__previous(interaction)

    @app_commands.command(
        name="unskip",
        description=app_commands.locale_str("Play the previous track from the queue"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def unskip(self, interaction: discord.Interaction):
        await self.__previous(interaction)

    async def __previous(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `previous` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).back(interaction.user, 0)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).previous()
        )
        self.__logger.debug(f"Successfully handled `previous` command (interaction:{interaction.id})")