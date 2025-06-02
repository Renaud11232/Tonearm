import logging
import sys

from tonearm.bot.cogs import *

import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import ServiceManager, PlayerManager, BotManager, ChatManager
from tonearm.bot.services import MetadataService, MediaService


class Tonearm:

    def __init__(self, discord_token: str, log_level: str, youtube_api_key: str | None, cobalt_api_url: str, cobalt_api_key: str | None):
        self.__discord_token = discord_token
        self.__log_level = log_level
        self.__init_logger("nextcord")
        self.__init_logger("tonearm")
        intents = nextcord.Intents.default()
        intents.voice_states = True
        activity = nextcord.Activity(
            type=nextcord.ActivityType.listening,
            name="/play"
        )
        self.__bot = commands.Bot(
            intents=intents,
            activity=activity
        )
        self.__service_manager = ServiceManager(
            PlayerManager(self.__bot, MetadataService(youtube_api_key), MediaService(cobalt_api_url, cobalt_api_key)),
            BotManager(self.__bot),
            ChatManager(self.__bot)
        )
        self.__init_cogs()

    def __init_logger(self, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(self.__log_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

    def __init_cogs(self):
        self.__bot.add_cog(ReadyListener(self.__service_manager))
        self.__bot.add_cog(VoiceStateChangeListener(self.__service_manager))
        self.__bot.add_cog(CleanCommand(self.__service_manager))
        self.__bot.add_cog(ClearCommand())
        self.__bot.add_cog(DebugCommand(self.__service_manager))
        self.__bot.add_cog(DjCommand())
        self.__bot.add_cog(ForwardCommand())
        self.__bot.add_cog(JoinCommand(self.__service_manager))
        self.__bot.add_cog(JumpCommand())
        self.__bot.add_cog(LeaveCommand(self.__service_manager))
        self.__bot.add_cog(LoopCommand())
        self.__bot.add_cog(MoveCommand())
        self.__bot.add_cog(NextCommand(self.__service_manager))
        self.__bot.add_cog(NowCommand())
        self.__bot.add_cog(PauseCommand())
        self.__bot.add_cog(PlayCommand(self.__service_manager))
        self.__bot.add_cog(PreviousCommand())
        self.__bot.add_cog(QueueCommand())
        self.__bot.add_cog(RemoveCommand())
        self.__bot.add_cog(ResumeCommand())
        self.__bot.add_cog(RewindCommand())
        self.__bot.add_cog(SeekCommand())
        self.__bot.add_cog(SettingCommand())
        self.__bot.add_cog(ShuffleCommand())
        self.__bot.add_cog(ShutdownCommand(self.__service_manager))
        self.__bot.add_cog(StopCommand(self.__service_manager))
        self.__bot.add_cog(VersionCommand())
        self.__bot.add_cog(VoteskipCommand())

    def run(self):
        self.__bot.run(self.__discord_token)
