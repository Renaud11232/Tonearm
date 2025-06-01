import nextcord
from nextcord.ext import commands

class VoteskipCommand(commands.Cog):

    @nextcord.slash_command(
        description="Votes to skip the current track"
    )
    async def voteskip(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")