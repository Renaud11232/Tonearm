import logging

from nextcord.ext import commands

class ReadyListener(commands.Cog):

    def __init__(self, bot: commands.Bot, logger: logging.Logger):
        super(ReadyListener, self).__init__()
        self.__bot = bot
        self.__logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        self.__logger.info(f"Tonearm is ready ! You can invite the bot with https://discordapp.com/oauth2/authorize?client_id={self.__bot.user.id}&scope=bot%20applications.commands&permissions=36700160")