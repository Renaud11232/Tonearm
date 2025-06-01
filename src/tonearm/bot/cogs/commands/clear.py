import nextcord
from nextcord.ext import commands

class ClearCommand(commands.Cog):

    @nextcord.slash_command(
        description="Clears all songs in the queue"
    )
    async def clear(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")