import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.cogs.transformers import ZeroIndexTransformer
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.base import InjectorCog


@singleton
class RemoveCommand(InjectorCog):

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
        name="remove",
        description=app_commands.locale_str("Remove a track from the queue"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        track=app_commands.locale_str("Track number to remove")
    )
    @app_commands.rename(
        track=app_commands.locale_str("track")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def remove(self,
                     interaction: discord.Interaction,
                     track: app_commands.Transform[int, ZeroIndexTransformer]):
        self.__logger.debug(f"Handling `remove` command (interaction:{interaction.id})")
        await interaction.response.defer()
        removed_track = await self.__player_manager.get(interaction.guild).remove(interaction.user, track)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).remove(removed_track)
        )
        self.__logger.debug(f"Successfully handled `remove` command (interaction:{interaction.id})")