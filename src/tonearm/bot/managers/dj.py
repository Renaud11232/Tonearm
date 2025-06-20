import nextcord

from injector import singleton, inject, Injector

from tonearm.bot.services import DjService

from .base import ManagerBase
from .storage import StorageManager


@singleton
class DjManager(ManagerBase[nextcord.Guild, DjService]):

    @inject
    def __init__(self, storage_manager: StorageManager, injector: Injector):
        super().__init__()
        self.__storage_manager = storage_manager
        self.__injector = injector

    async def _get_id(self, key: nextcord.Guild) -> int:
        return key.id

    async def _create(self, key: nextcord.Guild) -> DjService:
        return self.__injector.create_object(
            DjService,
            additional_kwargs={
                "storage_service": await self.__storage_manager.get(key)
            }
        )