import logging

import nextcord
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.services import BotService, EmbedService

from .base import CommandCogBase


@singleton
class ShutdownCommand(CommandCogBase):

    @inject
    def __init__(self, bot_service: BotService, embed_service: EmbedService):
        super().__init__()
        self.__bot_service = bot_service
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.shutdown, checks=[
            application_checks.is_owner()
        ])

    @nextcord.slash_command(
        name="shutdown",
        description="Shuts the bot down"
    )
    async def shutdown(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `shutdown` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await interaction.followup.send(
            embed=self.__embed_service.shutdown()
        )
        await self.__bot_service.shutdown()