import nextcord
from nextcord.ext import commands

from injector import singleton


@singleton
class DjCommand(commands.Cog):

    @nextcord.slash_command(
        description="Adds or removes a role to the DJ roles"
    )
    async def dj(self, interaction: nextcord.Interaction):
        pass

    @dj.subcommand(
        description="Adds a role to the DJ roles"
    )
    async def add(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")

    @dj.subcommand(
        description="Removes a role from the DJ roles"
    )
    async def remove(self, interaction: nextcord.Interaction):
        #TODO
        await interaction.send(":wrench: This feature is not implemented yet !")