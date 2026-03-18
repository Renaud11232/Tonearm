from injector import singleton, inject, Injector

import discord

from tonearm.bot.services import EmbedService

from .base import ManagerBase
from .storage import StorageManager


@singleton
class EmbedManager(ManagerBase[discord.Guild, EmbedService]):

    @inject
    def __init__(self, storage_manager: StorageManager, injector: Injector):
        super().__init__()
        self.__storage_manager = storage_manager
        self.__injector = injector

    def _get_id(self, key: discord.Guild) -> int:
        return key.id

    def _create(self, key: discord.Guild) -> EmbedService:
        return self.__injector.create_object(
            EmbedService,
            additional_kwargs={
                "storage_service": self.__storage_manager.get(key)
            }
        )