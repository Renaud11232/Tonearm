import logging

import nextcord
from nextcord.ext import commands

from tonearm.bot.cogs.converters import BadDuration
from tonearm.bot.exceptions import TonearmException


class ApplicationCommandErrorListener(commands.Cog):

    def __init__(self):
        super().__init__()
        self.__logger = logging.getLogger("tonearm.listeners")

    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        self.__logger.debug(f"Failed to handle command (interaction:{interaction.id}) due to exception : {repr(error)}")
        if isinstance(error, nextcord.ApplicationInvokeError):
            exception = error.original
            if isinstance(exception, TonearmException):
                await interaction.followup.send(f":x: {str(exception)}")
            elif isinstance(exception, BadDuration):
                #TODO
                pass
            else:
                raise error
        else:
            raise error