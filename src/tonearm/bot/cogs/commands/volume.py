import nextcord
from nextcord.ext import commands

class VolumeCommand(commands.Cog):

    @nextcord.slash_command(
        description="Changes the volume of the playing tracks"
    )
    async def volume(self, interaction: nextcord.Interaction, volume: int):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")