import nextcord
from nextcord.ext import commands

class Now(commands.Cog):

    @nextcord.slash_command(
        description="Shows the current playing track"
    )
    async def now(self, interaction: nextcord.Interaction):
        await self.__now(interaction)

    @nextcord.slash_command(
        description="Shows the current playing track"
    )
    async def now_playing(self, interaction: nextcord.Interaction):
        await self.__now(interaction)

    @staticmethod
    async def __now(interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")