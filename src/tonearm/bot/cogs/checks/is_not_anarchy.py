from injector import inject, noninjectable

import discord

from tonearm.bot.managers import StorageManager

from .internal import dependency_needing_check
from .exceptions import TranslatableCheckFailure


def is_not_anarchy():
    @inject
    @noninjectable("interaction")
    async def predicate(interaction: discord.Interaction, storage_manager: StorageManager) -> bool:
        if storage_manager.get(interaction.guild).get_anarchy():
            raise TranslatableCheckFailure("Anarchy rules here, votes are disabled !")
        return True
    return dependency_needing_check(predicate)
