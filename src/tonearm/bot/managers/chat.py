import discord

from injector import singleton, inject, Injector

from .base import ManagerBase
from tonearm.bot.services import ChatService


@singleton
class ChatManager(ManagerBase[discord.TextChannel, ChatService]):

    @inject
    def __init__(self, injector: Injector):
        super().__init__()
        self.__injector = injector

    def _get_id(self, key: discord.TextChannel) -> int:
        return key.id

    def _create(self, key: discord.TextChannel) -> ChatService:
        return self.__injector.create_object(
            ChatService,
            additional_kwargs={
                "channel": key
            }
        )
