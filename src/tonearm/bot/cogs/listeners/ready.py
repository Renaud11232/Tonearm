import logging

import nextcord
from nextcord.ext import commands

class ReadyListener(commands.Cog):

    def __init__(self, bot: commands.Bot, logger: logging.Logger):
        super(ReadyListener, self).__init__()
        self.__bot = bot
        self.__logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
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
        self.__logger.info(f"Tonearm is ready ! You can invite the bot with {nextcord.utils.oauth_url(self.__bot.user.id, scopes=scopes, permissions=permissions)}")