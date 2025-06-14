import nextcord
from nextcord.ext import commands

from injector import singleton


@singleton
class SettingCommand(commands.Cog):

    @nextcord.slash_command(
        description="Gets or sets setting values"
    )
    async def setting(self, interaction: nextcord.Interaction):
        pass

    @setting.subcommand(
        description="Gets the value of a given setting"
    )
    async def get(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")

    @setting.subcommand(
        description="Sets the value of a given setting"
    )
    async def set(self, interaction: nextcord.Interaction):
        #TODO
        #Handle at least : channel, anarchy mode
        await interaction.send(":wrench: This feature is not implemented yet !")