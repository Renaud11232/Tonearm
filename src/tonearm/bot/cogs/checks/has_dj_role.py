from injector import inject, noninjectable

import discord
from discord import app_commands

from tonearm.bot.managers import StorageManager

from .internal import dependency_needing_check, recover_predicates


def has_dj_role():
    @inject
    @noninjectable("interaction")
    async def predicate(interaction: discord.Interaction, storage_manager: StorageManager) -> bool:
        roles = storage_manager.get(interaction.guild).get_dj_roles()
        int_roles = list(map(lambda role: role.id, roles))
        return await discord.utils.maybe_coroutine(recover_predicates(app_commands.checks.has_any_role(*int_roles))[0], interaction)
    return dependency_needing_check(predicate)
