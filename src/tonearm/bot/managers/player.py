import nextcord

from injector import singleton, inject, Injector

from .base import ManagerBase
from tonearm.bot.services import PlayerService, MetadataService, MediaService


@singleton
class PlayerManager(ManagerBase[nextcord.Guild, PlayerService]):

    @inject
    def __init__(self, injector: Injector):
        super().__init__()
        self.__injector = injector

    def _get_id(self, key: nextcord.Guild) -> int:
        return key.id

    def _create(self, key: nextcord.Guild) -> PlayerService:
        return self.__injector.create_object(
            PlayerService,
            additional_kwargs={
                "guild": key
            }
        )