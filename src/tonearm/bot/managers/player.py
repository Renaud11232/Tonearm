import nextcord
from nextcord.ext import commands

from injector import inject, ProviderOf, singleton

from .base import ManagerBase
from tonearm.bot.services import PlayerService, MetadataService, MediaService


@singleton
class PlayerManager(ManagerBase[nextcord.Guild, PlayerService]):

    @inject
    def __init__(self, bot_provider: ProviderOf[commands.Bot], metadata_service: MetadataService, media_service: MediaService):
        super().__init__()
        self.__bot_provider = bot_provider
        self.__metadata_service = metadata_service
        self.__media_service = media_service

    def _get_id(self, key: nextcord.Guild) -> int:
        return key.id

    def _create(self, key: nextcord.Guild) -> PlayerService:
        return PlayerService(key, self.__bot_provider.get(), self.__metadata_service, self.__media_service)