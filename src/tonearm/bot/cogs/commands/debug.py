import logging

import nextcord
from nextcord.ext import commands, application_checks

from injector import inject, singleton

from tonearm.bot.managers import PlayerManager


@singleton
class DebugCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager):
        super().__init__()
        self.__player_manager = player_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Prints the current internal state of the bot for debugging purposes"
    )
    @application_checks.is_owner()
    #TODO: Delete this when its not needed anymore
    async def debug(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `debug` command (interaction:{interaction.id})")
        await interaction.response.defer(ephemeral=True)
        player_service = await self.__player_manager.get(interaction.guild)
        debug_data = await player_service.debug()
        await interaction.followup.send(
            f":tools: Here it is, I hope it will help :\n"
            f"```\n"
            f"{debug_data}\n"
            f"```\n"
        )
        self.__logger.debug(f"Successfully handled `debug` command (interaction:{interaction.id}), returning {repr(debug_data)}")