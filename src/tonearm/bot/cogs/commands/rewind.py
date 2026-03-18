import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.cogs.transformers import DurationTransformer
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class RewindCommand(CogBase):

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
        name="rewind",
        description="Rewind a specific amount of time into the track"
    )
    @app_commands.describe(
        duration="How far to rewind back into the track"
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def rewind(self,
                     interaction: discord.Interaction,
                     duration: app_commands.Transform[int, DurationTransformer]):
        self.__logger.debug(f"Handling `rewind` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).rewind(interaction.user, duration)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).rewind()
        )
        self.__logger.debug(f"Successfully handled `rewind` command (interaction:{interaction.id})")
