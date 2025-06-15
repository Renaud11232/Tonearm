import nextcord
from nextcord.ext import commands

from injector import singleton


@singleton
class BackCommand(commands.Cog):

    @nextcord.slash_command(
        description="Jumps back to a specific track in the history"
    )
    async def back(self, interaction: nextcord.Interaction):
        await self.__back(interaction)

    @nextcord.slash_command(
        description="Jumps back to a specific track in the history"
    )
    async def unskipto(self, interaction: nextcord.Interaction):
        await self.__back(interaction)

    async def __back(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")