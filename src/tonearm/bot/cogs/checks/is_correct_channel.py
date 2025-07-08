from injector import inject

import nextcord
from nextcord.ext import application_checks

from tonearm.bot.cogs.checks.exceptions import NotCorrectChannel
from tonearm.bot.managers import StorageManager

class IsCorrectChannel:

    @inject
    def __init__(self, storage_manager: StorageManager):
        self.__storage_manager = storage_manager

    def __call__(self):
        def predicate(interaction: nextcord.Interaction) -> bool:
            channel = self.__storage_manager.get(interaction.guild).get_channel()
            if channel is not None and channel.id != interaction.channel.id:
                raise NotCorrectChannel()
            return True
        return application_checks.check(predicate)