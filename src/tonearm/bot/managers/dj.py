import discord

from injector import singleton, inject, Injector

from tonearm.bot.services import DjService

from .base import ManagerBase
from .storage import StorageManager


@singleton
class DjManager(ManagerBase[discord.Guild, DjService]):

    @inject
    def __init__(self, storage_manager: StorageManager, injector: Injector):
        super().__init__()
        self.__storage_manager = storage_manager
        self.__injector = injector

    def _get_id(self, key: discord.Guild) -> int:
        return key.id

    def _create(self, key: discord.Guild) -> DjService:
        return self.__injector.create_object(
            DjService,
            additional_kwargs={
                "storage_service": self.__storage_manager.get(key)
            }
        )