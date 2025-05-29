import nextcord
from nextcord.ext import commands

class VersionCommand(commands.Cog):

    @nextcord.slash_command(
        description="Shows nerdy details about the bot"
    )
    async def version(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")