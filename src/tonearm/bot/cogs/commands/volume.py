import nextcord
from nextcord.ext import commands

from injector import singleton


@singleton
class VolumeCommand(commands.Cog):

    @nextcord.slash_command(
        description="Changes the volume of the playing tracks"
    )
    async def volume(self, interaction: nextcord.Interaction, volume: int):
        #TODO :sound: Volume’s now X%. Don’t blame me if it’s too loud !
        await interaction.send(":wrench: This feature is not implemented yet !")