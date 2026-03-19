import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import is_correct_channel, can_use_dj_command
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.base import InjectorCog


@singleton
class PauseCommand(InjectorCog):

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
        name="pause",
        description=app_commands.locale_str("Pause the currently playing track"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def pause(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `pause` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).pause(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).pause()
        )
        self.__logger.debug(f"Successfully handled `pause` command (interaction:{interaction.id}")