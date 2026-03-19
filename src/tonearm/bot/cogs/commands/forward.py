import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.cogs.transformers import DurationTransformer
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.base import InjectorCog


@singleton
class ForwardCommand(InjectorCog):

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
        name="forward",
        description=app_commands.locale_str("Forward a specific amount of time into the track"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        duration=app_commands.locale_str("How far to fast forward into the track")
    )
    @app_commands.rename(
        duration=app_commands.locale_str("duration")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def forward(self,
                      interaction: discord.Interaction,
                      duration: app_commands.Transform[int, DurationTransformer]):
        self.__logger.debug(f"Handling `forward` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).forward(interaction.user, duration)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).forward()
        )
        self.__logger.debug(f"Successfully handled `forward` command (interaction:{interaction.id})")