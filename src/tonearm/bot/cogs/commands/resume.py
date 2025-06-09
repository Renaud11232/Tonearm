import nextcord
from nextcord.ext import commands

class ResumeCommand(commands.Cog):

    @nextcord.slash_command(
        description="Resumes the currently paused track"
    )
    async def resume(self, interaction: nextcord.Interaction):
        #TODO :play_pause: Back in action ! Enjoy the tunes.
        #TODO The music never really stopped.
        await interaction.send(":wrench: This feature is not implemented yet !")