from injector import inject

import nextcord
from nextcord.ext import application_checks

from tonearm.bot.managers import StorageManager


class HasDjRole:

    @inject
    def __init__(self, storage_manager: StorageManager):
        self.__storage_manager = storage_manager

    def __call__(self):
        def predicate(interaction: nextcord.Interaction) -> bool:
            roles = self.__storage_manager.get(interaction.guild).get_dj_roles()
            int_roles = list(map(lambda role: role.id, roles))
            return application_checks.has_any_role(*int_roles).predicate(interaction)
        return application_checks.check(predicate)