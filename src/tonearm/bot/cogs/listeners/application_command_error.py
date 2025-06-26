import logging

import nextcord
from injector import inject, singleton
from nextcord.ext import commands
from nextcord.errors import ApplicationCheckFailure

from tonearm.bot.exceptions import TonearmCommandException
from tonearm.bot.services import EmbedService


@singleton
class ApplicationCommandErrorListener(commands.Cog):

    @inject
    def __init__(self, embed_service: EmbedService):
        super().__init__()
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.listeners")

    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        self.__logger.debug(f"Failed to handle command (interaction:{interaction.id}) due to exception : {repr(error)}")
        if isinstance(error, ApplicationCheckFailure):
            await interaction.send(
                ephemeral=True,
                embed=self.__embed_service.error("You don't have permission to use this command in this channel.")
            )
        elif isinstance(error, nextcord.ApplicationInvokeError):
            exception = error.original
            if isinstance(exception, TonearmCommandException):
                await interaction.followup.send(
                    embed=self.__embed_service.error(exception)
                )
            else:
                raise error
        else:
            raise error