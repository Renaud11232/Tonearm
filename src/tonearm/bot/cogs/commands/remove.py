import nextcord
from nextcord.ext import commands

from injector import singleton


@singleton
class RemoveCommand(commands.Cog):

    @nextcord.slash_command(
        description="Removes a track from the queue"
    )
    async def remove(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")