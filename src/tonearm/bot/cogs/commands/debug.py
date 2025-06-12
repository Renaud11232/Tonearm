import logging

import nextcord
from nextcord.ext import commands

from injector import inject

from tonearm.bot.managers import ServiceManager


class DebugCommand(commands.Cog):

    @inject
    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Prints the current internal state of the bot for debugging purposes"
    )
    #TODO: Delete this when its not needed anymore
    async def debug(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling debug command (interaction:{interaction.id})")
        await interaction.response.defer(ephemeral=True)
        debug_data = await self.__service_manager.get_player(interaction.guild).debug()
        await interaction.followup.send(
            f":tools: Here it is, I hope it will help :\n"
            f"```\n"
            f"{debug_data}\n"
            f"```\n"
        )
        self.__logger.debug(f"Successfully handled debug command (interaction:{interaction.id}), returning {repr(debug_data)}")