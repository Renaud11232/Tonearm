from .base import ManagerBase

import nextcord
from nextcord.ext import commands

from tonearm.bot.services import PlayerService, MetadataService, MediaService


class PlayerManager(ManagerBase[nextcord.Guild, PlayerService]):

    def __init__(self, bot: commands.Bot, metadata_service: MetadataService, media_service: MediaService):
        super().__init__()
        self.__bot = bot
        self.__metadata_service = metadata_service
        self.__media_service = media_service

    def _get_id(self, key: nextcord.Guild) -> int:
        return key.id

    def _create(self, key: nextcord.Guild) -> PlayerService:
        return PlayerService(key, self.__bot, self.__metadata_service, self.__media_service)