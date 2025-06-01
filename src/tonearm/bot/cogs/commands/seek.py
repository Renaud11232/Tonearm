import nextcord
from nextcord.ext import commands

class SeekCommand(commands.Cog):

    @nextcord.slash_command(
        description="Seeks to a specific time in the track"
    )
    async def seek(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")