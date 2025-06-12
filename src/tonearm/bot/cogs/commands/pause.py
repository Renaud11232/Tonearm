import nextcord
from nextcord.ext import commands

from injector import singleton


@singleton
class PauseCommand(commands.Cog):

    @nextcord.slash_command(
        description="Pauses the currently playing track"
    )
    async def pause(self, interaction: nextcord.Interaction):
        #TODO :pause_button: Playback paused. Take your time !
        #TODO Already paused. No need to rush.
        await interaction.send(":wrench: This feature is not implemented yet !")