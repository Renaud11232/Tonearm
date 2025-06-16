import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class QueueCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="show the current queue"
    )
    async def queue(self,
                    interaction: nextcord.Interaction,
                    page: int = SlashOption(required=False, default=1, min_value=1)):
        self.__logger.debug(f"Handling queue command (interaction:{interaction.id})")
        await interaction.response.defer()
        player_service = await self.__player_manager.get(interaction.guild)
        status = await player_service.queue(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.queue(status, page)
        )
        self.__logger.debug(f"Successfully handled queue command (interaction:{interaction.id}, with status : {repr(status)}")