import nextcord
from nextcord.ext import commands

from injector import singleton


@singleton
class MoveCommand(commands.Cog):

    @nextcord.slash_command(
        description="Moves the position of a track in the queue"
    )
    async def move(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")