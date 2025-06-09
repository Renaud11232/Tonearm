import nextcord
from nextcord.ext import commands

class VotenextCommand(commands.Cog):

    @nextcord.slash_command(
        description="Votes to skip the current track"
    )
    async def votenext(self, interaction: nextcord.Interaction):
        await self.__votenext(interaction)

    @nextcord.slash_command(
        description="Votes to skip the current track"
    )
    async def voteskip(self, interaction: nextcord.Interaction):
        await self.__votenext(interaction)

    async def __votenext(self, interaction: nextcord.Interaction):
        #TODO :ballot_box: We need Y - X more votes to skip this track.
        #TODO :track_next: Track skipped by popular demand!
        #TODO :x: You already voted to skip this track.
        await interaction.send(":wrench: This feature is not implemented yet !")
