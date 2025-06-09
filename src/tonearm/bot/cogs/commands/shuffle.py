import nextcord
from nextcord.ext import commands

class ShuffleCommand(commands.Cog):

    @nextcord.slash_command(
        description="Shuffles tracks in the queue"
    )
    async def shuffle(self, interaction: nextcord.Interaction):
        #TODO :twisted_rightwards_arrows: Shuffled the queue. I hope you like surprises !
        await interaction.send(":wrench: This feature is not implemented yet !")