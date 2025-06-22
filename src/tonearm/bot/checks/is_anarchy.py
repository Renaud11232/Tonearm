from injector import inject

import nextcord
from nextcord.ext import application_checks

from tonearm.bot.managers import StorageManager


class IsAnarchy:

    @inject
    def __init__(self, storage_manager: StorageManager):
        self.__storage_manager = storage_manager

    def __call__(self):
        def predicate(interaction: nextcord.Interaction) -> bool:
            return self.__storage_manager.get(interaction.guild).get_anarchy()
        return application_checks.check(predicate)
