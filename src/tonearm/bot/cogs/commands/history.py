import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import is_correct_channel
from tonearm.bot.cogs.transformers import ZeroIndexTransformer
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class HistoryCommand(CogBase):

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
        name="history",
        description=app_commands.locale_str("Show the previously played tracks"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        page=app_commands.locale_str("Page to display")
    )
    @app_commands.rename(
        page=app_commands.locale_str("page")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    async def history(self,
                      interaction: discord.Interaction,
                      page: app_commands.Transform[int, ZeroIndexTransformer] = 0):
        self.__logger.debug(f"Handling `history` command (interaction:{interaction.id})")
        await interaction.response.defer()
        previous_tracks = self.__player_manager.get(interaction.guild).history(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).history(previous_tracks, page)
        )
        self.__logger.debug(f"Successfully handled `history` command (interaction:{interaction.id}, with previous tracks : {repr(previous_tracks)}")