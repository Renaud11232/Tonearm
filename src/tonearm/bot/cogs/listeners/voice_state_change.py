import logging

import nextcord
from nextcord.ext import commands

from injector import inject, singleton

from tonearm.bot.managers import PlayerManager


@singleton
class VoiceStateChangeListener(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager):
        super().__init__()
        self.__player_manager = player_manager
        self.__logger = logging.getLogger("tonearm.listeners")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        self.__logger.debug(f"Handling voice_state_update event")
        await self.__player_manager.get(member.guild).on_voice_state_update(member, before, after)
        self.__logger.debug("Successfully handled voice state update event")
