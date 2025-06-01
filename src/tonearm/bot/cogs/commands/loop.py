import nextcord
from nextcord.ext import commands

class LoopCommand(commands.Cog):

    @nextcord.slash_command(
        description="Sets the loop mode of the current playback queue"
    )
    async def loop(self, interaction: nextcord.Interaction):
        await self.__loop(interaction)

    @nextcord.slash_command(
        description="Sets the loop mode of the current playback queue"
    )
    async def repeat(self, interaction: nextcord.Interaction):
        await self.__loop(interaction)

    @staticmethod
    async def __loop(interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")
