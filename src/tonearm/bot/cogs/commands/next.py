import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class NextCommand(CogBase):

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
        name="next",
        description=app_commands.locale_str("Skip the current playing track to the next one"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def next(self, interaction: discord.Interaction):
        await self.__next(interaction)

    @app_commands.command(
        name="skip",
        description=app_commands.locale_str("Skip the current playing track to the next one"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def skip(self, interaction: discord.Interaction):
        await self.__next(interaction)

    async def __next(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `next` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).jump(interaction.user, 0)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).next()
        )
        self.__logger.debug(f"Successfully handled `next` command (interaction:{interaction.id})")