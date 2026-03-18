import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.cogs.transformers import DurationTransformer
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class SeekCommand(CogBase):

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
        name="seek",
        description=app_commands.locale_str("Seek to a specific time in the track"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        duration=app_commands.locale_str("Where to seek in the track")
    )
    @app_commands.rename(
        duration=app_commands.locale_str("duration")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def seek(self,
                   interaction: discord.Interaction,
                   duration: app_commands.Transform[int, DurationTransformer]):
        self.__logger.debug(f"Handling `seek` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).seek(interaction.user, duration)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).seek()
        )
        self.__logger.debug(f"Successfully handled `seek` command (interaction:{interaction.id})")