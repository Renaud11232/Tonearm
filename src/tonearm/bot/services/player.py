import threading

import nextcord
from nextcord.ext import commands

from tonearm.exceptions import TonearmException


class PlayerService:

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__lock = threading.Lock()
        self.__voice_channel = None
        self.__voice_client = None

    @staticmethod
    def __check_member_in_voice_channel(voice: nextcord.VoiceState):
        if voice is None or voice.channel is None:
            raise TonearmException("You must join a voice channel first")

    async def join(self, voice: nextcord.VoiceState):
        with self.__lock:
            await self.__join(voice)

    async def __join(self, voice: nextcord.VoiceState):
        self.__check_member_in_voice_channel(voice)
        if self.__voice_channel is not None:
            raise TonearmException("Unable to join channel, I've already joined a voice channel")
        self.__voice_client = await voice.channel.connect()
        await voice.channel.guild.change_voice_state(channel=voice.channel, self_deaf=True)
        self.__voice_channel = voice.channel.id

    async def leave(self, voice: nextcord.VoiceState):
        with self.__lock:
            #TODO: Stop
            await self.__leave(voice)

    async def __leave(self, voice: nextcord.VoiceState):
        self.__check_member_in_voice_channel(voice)
        if self.__voice_channel != voice.channel.id:
            raise TonearmException("I'm not in your voice channel")
        await self.__voice_client.disconnect()
        self.__voice_channel = None
        self.__voice_client = None

