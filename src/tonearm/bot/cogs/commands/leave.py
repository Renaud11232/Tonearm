import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.base import InjectorCog


@singleton
class LeaveCommand(InjectorCog):

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
        name="leave",
        description=app_commands.locale_str("Leave the current voice channel"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def leave(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `leave` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).leave(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).leave()
        )
        self.__logger.debug(f"Successfully handled `leave` command (interaction:{interaction.id})")
