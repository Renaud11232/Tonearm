import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.cogs.checks import is_correct_channel
from tonearm.bot.managers import PlayerManager, EmbedManager
from tonearm.bot.cogs.base import InjectorCog


@singleton
class PlayCommand(InjectorCog):

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
        name="play",
        description=app_commands.locale_str("Play a track or playlist in your voice channel. You can provide link, or search for a track"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        query=app_commands.locale_str("Track or playlist to play. You can provide a link, or search for a track")
    )
    @app_commands.rename(
        query=app_commands.locale_str("query")
    )
    @app_commands.guild_only()
    @is_correct_channel()
    async def play(self,
                   interaction: discord.Interaction,
                   query: str):
        self.__logger.debug(f"Handling `play` command (interaction:{interaction.id})")
        await interaction.response.defer()
        tracks = await self.__player_manager.get(interaction.guild).play(interaction.user, query)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).play(tracks)
        )
        self.__logger.debug(f"Successfully handled `play` command (interaction:{interaction.id}), adding {len(tracks)} track(s) to the queue")