import nextcord
from nextcord.ext import commands

class Pause(commands.Cog):

    @nextcord.slash_command(
        description="Pauses the currently playing track"
    )
    async def pause(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")