import nextcord
from nextcord.ext import commands

class ResumeCommand(commands.Cog):

    @nextcord.slash_command(
        description="Resumes the currently paused track"
    )
    async def resume(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")