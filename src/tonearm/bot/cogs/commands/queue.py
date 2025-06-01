import nextcord
from nextcord.ext import commands

class QueueCommand(commands.Cog):

    @nextcord.slash_command(
        description="show the current queue"
    )
    async def queue(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")