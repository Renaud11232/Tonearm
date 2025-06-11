from injector import ProviderOf, inject

from .base import ManagerBase

import nextcord
from nextcord.ext import commands

from tonearm.bot.services import ChatService


class ChatManager(ManagerBase[nextcord.TextChannel, ChatService]):

    @inject
    def __init__(self, bot_provider: ProviderOf[commands.Bot]):
        super().__init__()
        self.__bot_provider = bot_provider

    def _get_id(self, key: nextcord.TextChannel) -> int:
        return key.id

    def _create(self, key: nextcord.TextChannel) -> ChatService:
        return ChatService(key, self.__bot_provider.get())