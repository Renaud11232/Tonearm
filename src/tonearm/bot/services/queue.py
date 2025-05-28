import threading

import nextcord
from nextcord.ext import commands

from tonearm.exceptions import TonearmException


class QueueService:

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__lock = threading.Lock()
        self.__voice_channel = None
        self.__voice_client = None

    async def join(self, member: nextcord.Member):
        with self.__lock:
            await self.__join(member)

    async def __join(self, member: nextcord.Member):
        self.__check_member_in_voice_channel(member)
        if self.__voice_client is not None:
            raise TonearmException("Unable to join channel, I've already joined a voice channel")
        self.__voice_client = await member.voice.channel.connect()
        self.__voice_channel = member.voice.channel.id

    @staticmethod
    def __check_member_in_voice_channel(member: nextcord.Member):
        if member.voice is None or member.voice.channel is None:
            raise TonearmException("You must join a voice channel first")

