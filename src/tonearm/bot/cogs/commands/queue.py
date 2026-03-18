import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import is_correct_channel
from tonearm.bot.cogs.transformers import ZeroIndexTransformer
from tonearm.bot.managers import PlayerManager, EmbedManager

from .base import CogBase


@singleton
class QueueCommand(CogBase):

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
        name="queue",
        description="Show the current queue"
    )
    @app_commands.describe(
        page="Page to display"
    )
    @app_commands.guild_only()
    @is_correct_channel()
    async def queue(self,
                    interaction: discord.Interaction,
                    page: app_commands.Transform[int, ZeroIndexTransformer] = 0):
        self.__logger.debug(f"Handling `queue` command (interaction:{interaction.id})")
        await interaction.response.defer()
        status = self.__player_manager.get(interaction.guild).queue(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).queue(status, page)
        )
        self.__logger.debug(f"Successfully handled `queue` command (interaction:{interaction.id}, with status : {repr(status)}")