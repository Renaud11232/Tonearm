import nextcord

from injector import inject

from .chat import ChatManager
from .player import PlayerManager
from tonearm.bot.services import PlayerService, ChatService


class ServiceManager:

    @inject
    def __init__(self, player_manager: PlayerManager, chat_manager: ChatManager):
        self.__player_manager = player_manager
        self.__chat_manager = chat_manager

    def get_player(self, guild: nextcord.Guild) -> PlayerService:
        return self.__player_manager.get(guild)

    def get_chat(self, channel: nextcord.TextChannel) -> ChatService:
        return self.__chat_manager.get(channel)
