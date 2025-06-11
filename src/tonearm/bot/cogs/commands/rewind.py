import logging

import nextcord
from nextcord.ext import commands

from injector import inject

from tonearm.bot.cogs.converters import Duration
from tonearm.bot.managers import ServiceManager


class RewindCommand(commands.Cog):

    @inject
    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Rewinds a specific amount of time into the track"
    )
    async def rewind(self, interaction: nextcord.Interaction, duration: str):
        await interaction.response.defer()
        duration = await Duration().convert(interaction, duration)
        self.__logger.debug(f"Handling rewind command (interaction:{interaction.id})")
        await self.__service_manager.get_player(interaction.guild).rewind(interaction.user, duration)
        await interaction.followup.send(f":rewind: That part was worth a second listen !")
        self.__logger.debug(f"Successfully handled rewind command (interaction:{interaction.id})")
