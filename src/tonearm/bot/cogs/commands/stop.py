import nextcord
from nextcord.ext import commands

class Stop(commands.Cog):

    @nextcord.slash_command(
        description="Stops the current playback"
    )
    async def stop(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")