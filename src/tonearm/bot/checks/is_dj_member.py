from injector import inject

import nextcord
from nextcord.ext import application_checks

from tonearm.bot.managers import StorageManager


class IsDjMember:

    @inject
    def __init__(self, storage_manager: StorageManager):
        self.__storage_manager = storage_manager

    def __call__(self):
        def predicate(interaction: nextcord.Interaction) -> bool:
            members = self.__storage_manager.get(interaction.guild).get_dj_members()
            int_members = list(map(lambda member: member.id, members))
            return interaction.user.id in int_members
        return application_checks.check(predicate)
