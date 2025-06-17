import os

import nextcord

from injector import singleton, inject, Injector

from tonearm.configuration import Configuration
from tonearm.bot.services import StorageService

from .base import ManagerBase


@singleton
class StorageManager(ManagerBase[nextcord.Guild, StorageService]):

    @inject
    def __init__(self, configuration: Configuration, injector: Injector):
        super().__init__()
        self.__configuration = configuration
        self.__injector = injector

    async def _get_id(self, key: nextcord.Guild) -> int:
        return key.id

    async def _create(self, key: nextcord.Guild) -> StorageService:
        return self.__injector.create_object(
            StorageService,
            additional_kwargs={
                "file_name": os.path.join(self.__configuration.data_path, "guilds", f"{key.id}.json")
            }
        )