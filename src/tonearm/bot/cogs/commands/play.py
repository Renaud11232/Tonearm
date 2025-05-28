import nextcord
from nextcord.ext import commands

class Play(commands.Cog):

    @nextcord.slash_command(
        description="Play a track or playlist in your voice channel. You can provide link, or search for a track"
    )
    async def play(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")