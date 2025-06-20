import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class PlayCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Play a track or playlist in your voice channel. You can provide link, or search for a track"
    )
    async def play(self, interaction: nextcord.Interaction, query: str):
        self.__logger.debug(f"Handling `play` command (interaction:{interaction.id})")
        await interaction.response.defer()
        player_service = await self.__player_manager.get(interaction.guild)
        tracks = await player_service.play(interaction.user, query)
        await interaction.followup.send(
            embed=self.__embed_service.play(tracks)
        )
        self.__logger.debug(f"Successfully handled `play` command (interaction:{interaction.id}), adding {len(tracks)} track(s) to the queue")