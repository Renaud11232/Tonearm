import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.base import InjectorCog


@singleton
class NowCommand(InjectorCog):

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
        name="now",
        description=app_commands.locale_str("Show the current playing track"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    async def now(self, interaction: discord.Interaction):
        await self.__now(interaction)

    @app_commands.command(
        name="now-playing",
        description=app_commands.locale_str("Show the current playing track"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    async def now_playing(self, interaction: discord.Interaction):
        await self.__now(interaction)

    async def __now(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `now` command (interaction:{interaction.id})")
        await interaction.response.defer()
        status = self.__player_manager.get(interaction.guild).now(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).now(status)
        )
        self.__logger.debug(f"Successfully handled `now` command (interaction:{interaction.id}, with status : {repr(status)}")