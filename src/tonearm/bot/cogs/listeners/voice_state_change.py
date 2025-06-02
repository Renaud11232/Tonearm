import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager


class VoiceStateChangeListener(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.listeners")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        self.__logger.debug(f"Handling voice_state_update event")
        await self.__service_manager.get_player(member.guild).on_voice_state_update(member, before, after)
        self.__logger.debug("Successfully handled voice state update event")
