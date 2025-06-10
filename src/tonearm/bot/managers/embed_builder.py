from .base import ManagerBase
from tonearm.bot.services import EmbedBuilderService


class EmbedBuilderManager(ManagerBase[str, EmbedBuilderService]):

    def _get_id(self, key: str) -> str:
        return key

    def _create(self, key: str) -> EmbedBuilderService:
        return EmbedBuilderService()