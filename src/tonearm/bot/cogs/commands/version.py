import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.services import EmbedService, BotService


@singleton
class VersionCommand(commands.Cog):

    @inject
    def __init__(self, bot_service: BotService, embed_service: EmbedService):
        super().__init__()
        self.__bot_service = bot_service
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Shows nerdy details about the bot"
    )
    async def version(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `version` command (interaction:{interaction.id})")
        await interaction.response.defer(ephemeral=True)
        version = await self.__bot_service.version()
        await interaction.followup.send(
            embed=self.__embed_service.version()
        )
        self.__logger.debug(f"Successfully handled `version` command (interaction:{interaction.id}), returning {repr(version)}")