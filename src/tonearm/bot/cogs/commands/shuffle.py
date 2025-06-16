import logging

import nextcord
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class ShuffleCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Shuffles tracks in the queue"
    )
    async def shuffle(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling shuffle command (interaction:{interaction.id})")
        await interaction.response.defer()
        player_service = await self.__player_manager.get(interaction.guild)
        await player_service.shuffle(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.shuffle()
        )
        self.__logger.debug(f"Successfully handled shuffle command (interaction:{interaction.id}")