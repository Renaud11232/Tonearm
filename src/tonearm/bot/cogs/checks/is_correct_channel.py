import discord

from injector import inject, noninjectable

from tonearm.bot.managers import StorageManager

from .internal import dependency_needing_check
from .exceptions import TranslatableCheckFailure


def is_correct_channel():
    @inject
    @noninjectable("interaction")
    async def predicate(interaction: discord.Interaction, storage_manager: StorageManager):
        channel = storage_manager.get(interaction.guild).get_channel()
        if channel is not None and channel.id != interaction.channel.id:
            raise TranslatableCheckFailure(
                "I'm only accepting commands in the {channel} channel.",
                channel=channel.mention
            )
        return True
    return dependency_needing_check(predicate)