import logging

import nextcord
from injector import inject
from nextcord.ext import commands, application_checks

from tonearm.bot.services import BotService


class ShutdownCommand(commands.Cog):

    @inject
    def __init__(self, bot_service: BotService):
        super().__init__()
        self.__bot_service = bot_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Shuts the bot down"
    )
    @application_checks.is_owner()
    async def shutdown(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling shutdown command (interaction:{interaction.id})")
        await interaction.send(":saluting_face: Initiating shutdown sequence... it’s been an honor.")
        await self.__bot_service.shutdown()