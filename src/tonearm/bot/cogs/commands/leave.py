import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import QueueManager
from tonearm.exceptions import TonearmException

class LeaveCommand(commands.Cog):

    def __init__(self, queue_manager: QueueManager):
        self.__queue_manager = queue_manager

    @nextcord.slash_command(
        description="Leaves the current voice channel"
    )
    async def leave(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        queue = self.__queue_manager.get_queue(interaction.guild)
        try:
            await queue.leave(interaction.user)
            await interaction.followup.send(f":wave: Goodbye !")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")