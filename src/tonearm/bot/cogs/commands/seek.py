import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.cogs.converters import Duration
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class SeekCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Seeks to a specific time in the track"
    )
    async def seek(self, interaction: nextcord.Interaction, duration: str):
        self.__logger.debug(f"Handling seek command (interaction:{interaction.id})")
        await interaction.response.defer()
        duration = await Duration().convert(interaction, duration)
        player_service = await self.__player_manager.get(interaction.guild)
        await player_service.seek(interaction.user, duration)
        await interaction.followup.send(
            embed=self.__embed_service.seek()
        )
        self.__logger.debug(f"Successfully handled seek command (interaction:{interaction.id})")