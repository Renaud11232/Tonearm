import logging

import nextcord
from injector import inject, singleton
from nextcord.ext import commands

from tonearm.bot.exceptions import TonearmInvokeException
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
        if isinstance(error, nextcord.ApplicationInvokeError):
            exception = error.original
            if isinstance(exception, TonearmInvokeException):
                await interaction.followup.send(
                    embed=self.__embed_service.error(exception)
                )
            else:
                raise error
        else:
            raise error