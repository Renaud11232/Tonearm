import nextcord

from injector import singleton, inject, Injector

from tonearm.bot.services import PlayerService

from .base import ManagerBase
from .storage import StorageManager
from .embed import EmbedManager


@singleton
class PlayerManager(ManagerBase[nextcord.Guild, PlayerService]):

    @inject
    def __init__(self, storage_manager: StorageManager, embed_manager: EmbedManager, injector: Injector):
        super().__init__()
        self.__storage_manager = storage_manager
        self.__embed_manager = embed_manager
        self.__injector = injector

    def _get_id(self, key: nextcord.Guild) -> int:
        return key.id

    def _create(self, key: nextcord.Guild) -> PlayerService:
        return self.__injector.create_object(
            PlayerService,
            additional_kwargs={
                "guild": key,
                "storage_service": self.__storage_manager.get(key),
                "embed_service": self.__embed_manager.get(key)
            }
        )