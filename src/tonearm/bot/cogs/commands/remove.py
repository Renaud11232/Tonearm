import nextcord
from nextcord.ext import commands

class Remove(commands.Cog):

    @nextcord.slash_command(
        description="Removes a track from the queue"
    )
    async def remove(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")