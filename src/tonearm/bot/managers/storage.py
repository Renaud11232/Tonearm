import os

import discord

from injector import singleton, inject, Injector

from tonearm.configuration import Configuration
from tonearm.bot.services import StorageService

from .base import ManagerBase


@singleton
class StorageManager(ManagerBase[discord.Guild, StorageService]):

    @inject
    def __init__(self, configuration: Configuration, injector: Injector):
        super().__init__()
        self.__configuration = configuration
        self.__injector = injector

    def _get_id(self, key: discord.Guild) -> int:
        return key.id

    def _create(self, key: discord.Guild) -> StorageService:
        return self.__injector.create_object(
            StorageService,
            additional_kwargs={
                "guild": key,
                "file_name": os.path.join(self.__configuration.data_path, "guilds", f"{key.id}.json")
            }
        )