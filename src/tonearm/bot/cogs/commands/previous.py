import nextcord
from nextcord.ext import commands

class Previous(commands.Cog):

    @nextcord.slash_command(
        description="Play the previous track from the queue"
    )
    async def previous(self, interaction: nextcord.Interaction):
        await self.__previous(interaction)

    @nextcord.slash_command(
        description="Play the previous track from the queue"
    )
    async def unskip(self, interaction: nextcord.Interaction):
        await self.__previous(interaction)

    @staticmethod
    async def __previous(interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")