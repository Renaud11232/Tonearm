import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import can_use_dj_command, is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.base import InjectorCog


@singleton
class VolumeCommand(InjectorCog):

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
        name="volume",
        description=app_commands.locale_str("Change the volume of the playing tracks"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        value=app_commands.locale_str("Playback volume (between 0 and 200)")
    )
    @app_commands.rename(
        value=app_commands.locale_str("value")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @can_use_dj_command()
    async def volume(self,
                     interaction: discord.Interaction,
                     value: app_commands.Range[int, 0, 200]):
        self.__logger.debug(f"Handling `volume` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).volume(interaction.user, value)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).volume(value)
        )
        self.__logger.debug(f"Successfully handled `volume` command (interaction:{interaction.id}, setting volume to : {repr(value)}")