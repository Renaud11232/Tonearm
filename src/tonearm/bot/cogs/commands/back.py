import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.transformers import ZeroIndexTransformer

from .base import CogBase


@singleton
class BackCommand(CogBase):

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
        name="back",
        description=app_commands.locale_str("Jump back to a specific track in the history"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        track=app_commands.locale_str("Track number to jump back to"),
    )
    @app_commands.rename(
        track=app_commands.locale_str("track")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def back(self,
                   interaction: discord.Interaction,
                   track: app_commands.Transform[int, ZeroIndexTransformer]):
        await self.__back(interaction, track)


    @app_commands.command(
        name="unskipto",
        description=app_commands.locale_str("Jump back to a specific track in the history"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        track=app_commands.locale_str("Track number to jump back to")
    )
    @app_commands.rename(
        track=app_commands.locale_str("track")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def unskipto(self,
                       interaction: discord.Interaction,
                       track: app_commands.Transform[int, ZeroIndexTransformer]):
        await self.__back(interaction, track)

    async def __back(self, interaction: discord.Interaction, track: int):
        self.__logger.debug(f"Handling `back` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).back(interaction.user, track)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).back(track)
        )
        self.__logger.debug(f"Successfully handled `back` command (interaction:{interaction.id})")
