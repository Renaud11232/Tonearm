from injector import inject, noninjectable

import discord

from tonearm.bot.managers import StorageManager

from .internal import dependency_needing_check


def is_dj_member():
    @inject
    @noninjectable("interaction")
    async def predicate(interaction: discord.Interaction, storage_manager: StorageManager) -> bool:
        members = storage_manager.get(interaction.guild).get_dj_members()
        int_members = list(map(lambda member: member.id, members))
        return interaction.user.id in int_members
    return dependency_needing_check(predicate)
