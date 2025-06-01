import nextcord
from nextcord.ext import commands

class ForwardCommand(commands.Cog):

    @nextcord.slash_command(
        description="Forwards a specific amount of time into the track"
    )
    async def forward(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")