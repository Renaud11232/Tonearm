import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import is_correct_channel
from tonearm.bot.managers import EmbedManager
from tonearm.bot.services import BotService
from tonearm.bot.cogs.base import InjectorCog


@singleton
class VersionCommand(InjectorCog):

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
        name="version",
        description=app_commands.locale_str("Show nerdy details about the bot"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    async def version(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `version` command (interaction:{interaction.id})")
        await interaction.response.defer()
        version = self.__bot_service.version()
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).version(version)
        )
        self.__logger.debug(f"Successfully handled `version` command (interaction:{interaction.id}), returning {repr(version)}")