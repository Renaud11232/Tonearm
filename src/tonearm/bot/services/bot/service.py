import logging
import importlib.metadata

import nextcord
from nextcord.ext import commands

from injector import ProviderOf, inject, singleton

from .version import TonearmVersion


@singleton
class BotService:

    @inject
    def __init__(self, bot_provider: ProviderOf[commands.Bot]):
        self.__bot_provider = bot_provider
        self.__logger = logging.getLogger("tonearm.bot")

    async def shutdown(self):
        self.__logger.info("Shutdown requested. Goodbye !")
        await self.__bot_provider.get().close()

    def on_ready(self):
        scopes = [
            "bot",
            "applications.commands"
        ]
        permissions = nextcord.Permissions.none()
        permissions.update(
            connect=True,
            speak=True,
            use_voice_activation=True
        )
        invite_url = nextcord.utils.oauth_url(
            self.__bot_provider.get().user.id,
            scopes=scopes,
            permissions=permissions
        )
        self.__logger.info(f"Tonearm is ready ! You can invite the bot with {invite_url}")

    @staticmethod
    def version() -> TonearmVersion:
        metadata = importlib.metadata.metadata("Tonearm")
        version = metadata.get("Version")
        author_emails = metadata.get_all("Author-email") or []
        authors = list(map(lambda email: email.split(" <")[0], author_emails))
        project_urls = metadata.get_all("Project-URL") or []
        homepage = next((url[10:] for url in project_urls if url.startswith("homepage, ")), None)
        return TonearmVersion(
            version=version,
            authors=authors,
            homepage=homepage
        )
