import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class JoinCommand(CogBase):

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
        name="join",
        description=app_commands.locale_str("Join your current voice channel"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    async def join(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `join` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).join(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).join()
        )
        self.__logger.debug(f"Successfully handled `join` command (interaction:{interaction.id})")