import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.managers import ChatManager
from tonearm.bot.services import EmbedService


@singleton
class CleanCommand(commands.Cog):

    @inject
    def __init__(self, chat_manager: ChatManager, embed_service: EmbedService):
        super().__init__()
        self.__chat_manager = chat_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    #TODO: Translate commands and messages
    #TODO: Implements checks and permissions
    #TODO: Option documentation
    @nextcord.slash_command(
        description="Deletes bot messages in the channel (up to 100 at once)"
    )
    async def clean(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `clean` command (interaction:{interaction.id})")
        await interaction.response.defer(ephemeral=True)
        chat_service = await self.__chat_manager.get(interaction.channel)
        messages = await chat_service.clean()
        await interaction.followup.send(
            embed=self.__embed_service.clean()
        )
        self.__logger.debug(f"Successfully handled `clean` command (interaction:{interaction.id}), deleting {len(messages)} messages")