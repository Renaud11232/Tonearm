import discord

from injector import inject, noninjectable

from tonearm.bot.managers import StorageManager

from .internal import dependency_needing_check


def is_anarchy():
    @inject
    @noninjectable("interaction")
    async def predicate(interaction: discord.Interaction, storage_manager: StorageManager) -> bool:
        return storage_manager.get(interaction.guild).get_anarchy()
    return dependency_needing_check(predicate)
