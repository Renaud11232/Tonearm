import nextcord
from nextcord.ext import commands

from injector import singleton


@singleton
class VersionCommand(commands.Cog):

    @nextcord.slash_command(
        description="Shows nerdy details about the bot"
    )
    async def version(self, interaction: nextcord.Interaction):
        #TODO :computer: Tonearm version: vX.Y.Z — crafted with :heart: by Renaud11232. Up and running !
        await interaction.send(":wrench: This feature is not implemented yet !")