import nextcord
from nextcord.ext import commands

class Next(commands.Cog):

    @nextcord.slash_command(
        description="Skips the current playing track to the next one"
    )
    async def next(self, interaction: nextcord.Interaction):
        await self.__next(interaction)

    @nextcord.slash_command(
        description="Skips the current playing track to the next one"
    )
    async def skip(self, interaction: nextcord.Interaction):
        await self.__next(interaction)

    @staticmethod
    async def __next(interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")