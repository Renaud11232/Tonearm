import logging

import nextcord
from nextcord.ext import commands, application_checks

from injector import inject, singleton

from tonearm.bot.services import BotService, EmbedService


@singleton
class ShutdownCommand(commands.Cog):

    @inject
    def __init__(self, bot_service: BotService, embed_service: EmbedService):
        super().__init__()
        self.__bot_service = bot_service
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Shuts the bot down"
    )
    @application_checks.is_owner()
    async def shutdown(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling shutdown command (interaction:{interaction.id})")
        await interaction.response.defer()
        await interaction.followup.send(
            embed=self.__embed_service.shutdown()
        )
        await self.__bot_service.shutdown()