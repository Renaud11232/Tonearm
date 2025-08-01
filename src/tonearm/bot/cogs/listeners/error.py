import logging
import sys
from typing import cast

import nextcord
from injector import inject, singleton
from nextcord.ext import commands

from tonearm.bot.exceptions import TonearmConverterException
from tonearm.bot.managers import EmbedManager

@singleton
class ErrorListener(commands.Cog):

    @inject
    def __init__(self, embed_manager: EmbedManager):
        super().__init__()
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.listeners")

    async def on_error(self, event: str, *args, **kwargs):
        exception = sys.exception()
        if isinstance(exception, TonearmConverterException):
            interaction, = cast(tuple[nextcord.Interaction,], args)
            await interaction.send(
                ephemeral=True,
                embed=self.__embed_manager.get(interaction.guild).error(exception)
            )
        else:
            self.__logger.exception(f"Ignoring exception in {event}")