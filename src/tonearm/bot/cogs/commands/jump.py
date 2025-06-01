import nextcord
from nextcord.ext import commands

class JumpCommand(commands.Cog):

    @nextcord.slash_command(
        description="Jumps to a specific track in the queue"
    )
    async def jump(self, interaction: nextcord.Interaction):
        await self.__jump(interaction)

    @nextcord.slash_command(
        description="Jumps to a specific track in the queue"
    )
    async def skipto(self, interaction: nextcord.Interaction):
        await self.__jump(interaction)

    @staticmethod
    async def __jump(interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")