import logging

import nextcord
from nextcord.ext import commands

from injector import inject

from tonearm.bot.managers import ServiceManager


class JoinCommand(commands.Cog):

    @inject
    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Joins your current voice channel"
    )
    async def join(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        self.__logger.debug(f"Handling join command (interaction:{interaction.id})")
        await self.__service_manager.get_player(interaction.guild).join(interaction.user)
        await interaction.followup.send(f":party_popper: Let's get this party started !")
        self.__logger.debug(f"Successfully handled join command (interaction:{interaction.id})")