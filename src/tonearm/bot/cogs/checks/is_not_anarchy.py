from injector import inject

import nextcord
from nextcord.ext import application_checks

from tonearm.bot.cogs.checks.exceptions import IsAnarchy
from tonearm.bot.managers import StorageManager


class IsNotAnarchy:

    @inject
    def __init__(self, storage_manager: StorageManager):
        self.__storage_manager = storage_manager

    def __call__(self):
        def predicate(interaction: nextcord.Interaction) -> bool:
            if self.__storage_manager.get(interaction.guild).get_anarchy():
                raise IsAnarchy()
            return True
        return application_checks.check(predicate)
