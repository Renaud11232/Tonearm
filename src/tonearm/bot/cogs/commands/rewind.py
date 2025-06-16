import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.cogs.converters import Duration
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class RewindCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Rewinds a specific amount of time into the track"
    )
    async def rewind(self, interaction: nextcord.Interaction, duration: str):
        self.__logger.debug(f"Handling rewind command (interaction:{interaction.id})")
        await interaction.response.defer()
        duration = await Duration().convert(interaction, duration)
        player_service = await self.__player_manager.get(interaction.guild)
        await player_service.rewind(interaction.user, duration)
        await interaction.followup.send(
            embed=self.__embed_service.rewind()
        )
        self.__logger.debug(f"Successfully handled rewind command (interaction:{interaction.id})")
