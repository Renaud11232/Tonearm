import nextcord
from nextcord.ext import commands

class Rewind(commands.Cog):

    @nextcord.slash_command(
        description="Rewinds a specific amount of time into the track"
    )
    async def rewind(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")