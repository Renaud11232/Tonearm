from .base import ManagerBase

from tonearm.bot.services import BotService

from nextcord.ext import commands

class BotManager(ManagerBase[str, BotService]):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.__bot = bot

    def _get_id(self, key: str) -> str:
        return key

    def _create(self, key: str) -> BotService:
        return BotService(self.__bot)

