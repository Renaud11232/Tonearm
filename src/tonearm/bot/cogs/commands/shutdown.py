import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import is_owner
from tonearm.bot.services import BotService
from tonearm.bot.managers import EmbedManager

from .base import CogBase


@singleton
class ShutdownCommand(CogBase):

    @inject
    def __init__(self,
                 bot_service: BotService,
                 embed_manager: EmbedManager,
                 injector: Injector):
        super().__init__(injector)
        self.__bot_service = bot_service
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @app_commands.command(
        name="shutdown",
        description="Shut the bot down"
    )
    @app_commands.guild_only()
    @is_owner()
    async def shutdown(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `shutdown` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).shutdown()
        )
        await self.__bot_service.shutdown()