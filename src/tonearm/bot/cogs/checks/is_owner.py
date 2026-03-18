import discord
from discord.ext import commands

from injector import inject, noninjectable

from .internal import dependency_needing_check


def is_owner():
    @inject
    @noninjectable("interaction")
    async def predicate(interaction: discord.Interaction, bot: commands.Bot) -> bool:
        return await bot.is_owner(interaction.user)
    return dependency_needing_check(predicate)
