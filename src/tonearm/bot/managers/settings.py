import nextcord

from injector import singleton, inject, Injector

from tonearm.bot.services import SettingsService

from .base import ManagerBase
from .storage import StorageManager


@singleton
class SettingsManager(ManagerBase[nextcord.Guild, SettingsService]):

    @inject
    def __init__(self, storage_manager: StorageManager, injector: Injector):
        super().__init__()
        self.__storage_manager = storage_manager
        self.__injector = injector

    async def _get_id(self, key: nextcord.Guild) -> int:
        return key.id

    async def _create(self, key: nextcord.Guild) -> SettingsService:
        return self.__injector.create_object(
            SettingsService,
            additional_kwargs={
                "storage_service": await self.__storage_manager.get(key)
            }
        )