import nextcord
from nextcord.ext import commands

class Leave(commands.Cog):

    @nextcord.slash_command(
        description="Leaves the current voice channel"
    )
    async def leave(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")