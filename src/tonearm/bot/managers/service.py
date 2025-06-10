import nextcord

from .chat import ChatManager
from .player import PlayerManager
from .bot import BotManager
from .embed_builder import EmbedBuilderManager
from tonearm.bot.services import PlayerService, ChatService, BotService, EmbedBuilderService


class ServiceManager:

    def __init__(self, player_manager: PlayerManager, bot_manager: BotManager, chat_manager: ChatManager, embed_builder: EmbedBuilderManager):
        self.__player_manager = player_manager
        self.__bot_manager = bot_manager
        self.__chat_manager = chat_manager
        self.__embed_builder = embed_builder

    def get_player(self, guild: nextcord.Guild) -> PlayerService:
        return self.__player_manager.get(guild)

    def get_bot(self) -> BotService:
        return self.__bot_manager.get("__bot_service__")

    def get_chat(self, channel: nextcord.TextChannel) -> ChatService:
        return self.__chat_manager.get(channel)

    def get_embed_builder(self) -> EmbedBuilderService:
        return self.__embed_builder.get("__embed_builder_service__")
