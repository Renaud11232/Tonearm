from injector import inject, noninjectable

import discord

from tonearm.bot.cogs.checks.exceptions import IsAnarchy
from tonearm.bot.managers import StorageManager

from .internal import dependency_needing_check


def is_not_anarchy():
    @inject
    @noninjectable("interaction")
    async def predicate(interaction: discord.Interaction, storage_manager: StorageManager) -> bool:
        if storage_manager.get(interaction.guild).get_anarchy():
            raise IsAnarchy()
        return True
    return dependency_needing_check(predicate)
