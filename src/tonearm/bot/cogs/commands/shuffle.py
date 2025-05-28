import nextcord
from nextcord.ext import commands

class Shuffle(commands.Cog):

    @nextcord.slash_command(
        description="Shuffles tracks in the queue"
    )
    async def shuffle(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")