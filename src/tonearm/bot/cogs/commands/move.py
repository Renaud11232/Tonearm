import nextcord
from nextcord.ext import commands

class Move(commands.Cog):

    @nextcord.slash_command(
        description="Moves the position of a track in the queue"
    )
    async def move(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")