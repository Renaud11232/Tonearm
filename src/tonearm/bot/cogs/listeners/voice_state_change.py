import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager


class VoiceStateChangeListener(commands.Cog):

    def __init__(self, bot: commands.Bot, service_manager: ServiceManager):
        super().__init__()
        self.__bot = bot
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.listeners")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        player = self.__service_manager.get_player(member.guild)
        if before.channel != after.channel:
            self.__logger.debug(f"Member {member.id} moved from voice channel {repr(before.channel)} to {repr(after.channel)}")
            if before.channel is not None:
                if member.id != self.__bot.user.id:
                    await player.on_user_moved(before.channel)
                elif after.channel is None:
                    await player.on_bot_disconnected()
                else:
                    await player.on_bot_moved()
