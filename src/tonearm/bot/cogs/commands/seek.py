import logging

import nextcord
from nextcord.ext import commands

from injector import inject

from tonearm.bot.cogs.converters import Duration
from tonearm.bot.managers import ServiceManager


class SeekCommand(commands.Cog):

    @inject
    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Seeks to a specific time in the track"
    )
    async def seek(self, interaction: nextcord.Interaction, duration: str):
        self.__logger.debug(f"Handling seek command (interaction:{interaction.id})")
        await interaction.response.defer()
        duration = await Duration().convert(interaction, duration)
        await self.__service_manager.get_player(interaction.guild).seek(interaction.user, duration)
        await interaction.followup.send(f":dart: Dropping the needle, classic move.")
        self.__logger.debug(f"Successfully handled seek command (interaction:{interaction.id})")