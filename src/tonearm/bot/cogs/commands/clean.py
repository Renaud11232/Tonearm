import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager


class CleanCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    #TODO: Translate commands and messages
    #TODO: Implements checks and permissions
    #TODO: Option documentation
    @nextcord.slash_command(
        description="Deletes bot messages in the channel (up to 100 at once)"
    )
    async def clean(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling clean command (interaction:{interaction.id})")
        await interaction.response.defer(ephemeral=True)
        messages = await self.__service_manager.get_chat(interaction.channel).clean()
        await interaction.followup.send(f":wastebasket: Finished cleaning messages ({len(messages)})")
        self.__logger.debug(f"Successfully handled clean command (interaction:{interaction.id}), deleting {len(messages)} messages")