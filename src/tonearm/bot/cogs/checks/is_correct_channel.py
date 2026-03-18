import discord

from injector import inject, noninjectable

from tonearm.bot.cogs.checks.exceptions import NotCorrectChannel
from tonearm.bot.managers import StorageManager

from .internal import dependency_needing_check


def is_correct_channel():
    @inject
    @noninjectable("interaction")
    async def predicate(interaction: discord.Interaction, storage_manager: StorageManager):
        channel = storage_manager.get(interaction.guild).get_channel()
        if channel is not None and channel.id != interaction.channel.id:
            raise NotCorrectChannel()
        return True
    return dependency_needing_check(predicate)