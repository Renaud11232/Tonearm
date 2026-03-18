import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.cogs.transformers import ZeroIndexTransformer
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class MoveCommand(CogBase):

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
        name="move",
        description=app_commands.locale_str("Change the position of a track in the queue"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        from_=app_commands.locale_str("Initial track position"),
        to=app_commands.locale_str("Target track position")
    )
    @app_commands.rename(
        from_=app_commands.locale_str("from"),
        to=app_commands.locale_str("to")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def move(self,
                   interaction: discord.Interaction,
                   from_: app_commands.Transform[int, ZeroIndexTransformer],
                   to: app_commands.Transform[int, ZeroIndexTransformer]):
        self.__logger.debug(f"Handling `move` command (interaction:{interaction.id})")
        await interaction.response.defer()
        moved_track = await self.__player_manager.get(interaction.guild).move(interaction.user, from_, to)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).move(moved_track, from_, to)
        )
        self.__logger.debug(f"Successfully handled `move` command (interaction:{interaction.id})")