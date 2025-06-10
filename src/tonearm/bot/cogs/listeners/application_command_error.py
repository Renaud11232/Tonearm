import logging

import nextcord
from nextcord.ext import commands

from tonearm.bot.exceptions import TonearmException
from tonearm.bot.managers import ServiceManager


class ApplicationCommandErrorListener(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.listeners")

    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        self.__logger.debug(f"Failed to handle command (interaction:{interaction.id}) due to exception : {repr(error)}")
        if isinstance(error, nextcord.ApplicationInvokeError):
            exception = error.original
            if isinstance(exception, TonearmException):
                await interaction.followup.send(f":x: {str(exception)}")
            else:
                raise error
        else:
            raise error