import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.transformers import LoopModeTransformer
from tonearm.bot.services.player import LoopMode

from .base import CogBase


@singleton
class LoopCommand(CogBase):

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
        name="loop",
        description=app_commands.locale_str("Set the loop mode of the current playback queue"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        mode=app_commands.locale_str("Loop mode to use")
    )
    @app_commands.rename(
        mode=app_commands.locale_str("mode")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def loop(self,
                   interaction: discord.Interaction,
                   mode: app_commands.Transform[LoopMode, LoopModeTransformer]):
        await self.__loop(interaction, mode)

    @app_commands.command(
        name="repeat",
        description=app_commands.locale_str("Set the loop mode of the current playback queue"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        mode=app_commands.locale_str("Loop mode to use")
    )
    @app_commands.rename(
        mode=app_commands.locale_str("mode")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def repeat(self,
                     interaction: discord.Interaction,
                     mode: app_commands.Transform[LoopMode, LoopModeTransformer]):
        await self.__loop(interaction, mode)

    async def __loop(self, interaction: discord.Interaction, mode: LoopMode):
        self.__logger.debug(f"Handling `loop` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).loop(interaction.user, mode)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).loop(mode)
        )
        self.__logger.debug(f"Successfully handled `loop` command (interaction:{interaction.id})")
