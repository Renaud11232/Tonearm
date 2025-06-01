import math
from typing import List
import time
import asyncio
import logging

import nextcord
from nextcord.ext import commands

from tonearm.bot.audiosource import ControllableFFmpegPCMAudio
from tonearm.bot.services.metadata import MetadataService
from tonearm.bot.services.media import MediaService
from tonearm.bot.data import TrackMetadata
from tonearm.exceptions import TonearmException


class PlayerService:

    def __init__(self, guild: nextcord.Guild, bot: commands.Bot, metadata_service: MetadataService, media_service: MediaService):
        self.__guild = guild
        self.__bot = bot
        self.__metadata_service = metadata_service
        self.__media_service = media_service
        self.__logger = logging.getLogger("tonearm.player")
        self.__lock = asyncio.Lock()
        self.__previous_tracks = []
        self.__current_track = None
        self.__next_tracks = []
        self.__audio_source = None
        self.__stopped = False
        self.__graceful_leave = False
        self.__last_leave = None

    @property
    def __voice_client(self) -> nextcord.VoiceClient | None:
        protocol = nextcord.utils.get(self.__bot.voice_clients, guild=self.__guild)
        if isinstance(protocol, nextcord.VoiceClient):
            return protocol
        return None

    @staticmethod
    def __check_member_in_voice_channel(member: nextcord.Member):
        if member.voice is None or member.voice.channel is None:
            raise TonearmException("You must join a voice channel first")

    def __check_same_voice_channel(self, member: nextcord.Member):
        if self.__voice_client is None or member.voice.channel != self.__voice_client.channel:
            raise TonearmException("I'm not in your voice channel")

    def __check_active_audio_source(self):
        if not self.__is_playing():
            raise TonearmException("I'm not currently playing any track")

    def __is_connected(self):
        return self.__voice_client is not None and self.__voice_client.is_connected()

    def __is_playing(self):
        return self.__voice_client is not None and self.__voice_client.is_playing()

    def __check_not_in_voice_channel(self):
        if self.__is_connected():
            raise TonearmException("I've already joined a voice channel")

    async def join(self, member: nextcord.Member):
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_not_in_voice_channel()
            await self.__safe_join(member.voice.channel)

    async def __safe_join(self, channel: nextcord.VoiceChannel):
        if not self.__graceful_leave and  self.__last_leave is not None and time.time() < self.__last_leave + 60:
            raise TonearmException(f"I can't join right now, please try again in {math.floor(self.__last_leave + 60 - time.time())} seconds")
        if self.__is_connected():
            await self.__voice_client.disconnect(force=True)
        await channel.connect()
        await channel.guild.change_voice_state(
            channel=channel,
            self_deaf=True
        )
        self.__graceful_leave = False

    async def play(self, member: nextcord.Member, query: str) -> List[TrackMetadata]:
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            if not self.__is_connected():
                await self.__safe_join(member.voice.channel)
            self.__check_same_voice_channel(member)
            tracks = await self.__metadata_service.fetch(query)
            if len(tracks) == 0:
                raise TonearmException("No playable track were found")
            self.__next_tracks.extend(tracks)
            if self.__current_track is None:
                self.__safe_switch_to_next_track()
                await self.__safe_start_playing()
            return tracks

    def __safe_switch_to_next_track(self):
        if self.__current_track is not None and not self.__stopped:
            self.__previous_tracks.append(self.__current_track)
        if len(self.__next_tracks) == 0:
            self.__current_track = None
        else:
            self.__current_track = self.__next_tracks.pop(0)

    async def __safe_start_playing(self):
        if self.__current_track is not None:
            self.__stopped = False
            stream_url = await self.__media_service.fetch(self.__current_track.url)
            self.__audio_source = ControllableFFmpegPCMAudio(stream_url)
            self.__voice_client.play(
                self.__audio_source,
                after=self.__on_audio_source_ended
            )

    async def __on_audio_source_ended(self, _):
        self.__audio_source = None
        self.__safe_switch_to_next_track()
        await self.__safe_start_playing()

    async def next(self, member: nextcord.Member):
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_stop_current_track()

    def __safe_stop_current_track(self):
        if self.__voice_client is not None:
            self.__voice_client.stop()

    async def stop(self, member: nextcord.Member):
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            await self.__safe_stop()

    async def __safe_stop(self):
        self.__stopped = True
        self.__next_tracks.clear()
        self.__safe_stop_current_track()
        self.__previous_tracks.clear()

    async def leave(self, member: nextcord.Member):
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__safe_leave()

    async def __safe_leave(self):
        self.__graceful_leave = True
        await self.__safe_stop()
        if self.__voice_client is not None:
            await self.__voice_client.disconnect()

    def __is_alone(self, channel: nextcord.VoiceChannel) -> bool:
        others = [m for m in channel.members if m.id != self.__bot.user.id]
        return len(others) == 0

    async def on_bot_disconnected(self):
        await self.__safe_stop()
        self.__last_leave = time.time()

    async def on_bot_moved(self):
        async with self.__lock:
            while not self.__is_connected():
                await asyncio.sleep(0.1)
            await self.__safe_leave()

    async def on_user_moved(self, from_channel: nextcord.VoiceChannel):
        async with self.__lock:
            if self.__is_connected() and self.__voice_client.channel == from_channel and self.__is_alone(from_channel):
                await self.__safe_leave()