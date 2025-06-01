import threading
from typing import List

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
        self.__lock = threading.Lock()
        self.__previous_tracks = []
        self.__current_track = None
        self.__next_tracks = []
        self.__audio_source = None
        self.__stopped = False

    @staticmethod
    def __check_member_in_voice_channel(member: nextcord.Member):
        if member.voice is None or member.voice.channel is None:
            raise TonearmException("You must join a voice channel first")

    def __check_same_voice_channel(self, member: nextcord.Member):
        if self.__guild.voice_client is None or member.voice.channel != self.__guild.voice_client.channel:
            raise TonearmException("I'm not in your voice channel")

    def __check_active_audio_source(self):
        if self.__guild.voice_client is None or not self.__guild.voice_client.is_playing():
            raise TonearmException("I'm not currently playing any track")

    def __check_not_in_voice_channel(self):
        if self.__guild.voice_client is not None and self.__guild.voice_client.is_connected():
            raise TonearmException("I've already joined a voice channel")

    async def join(self, member: nextcord.Member):
        with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_not_in_voice_channel()
            await self.__safe_join(member.voice.channel)

    async def __safe_join(self, channel: nextcord.VoiceChannel):
        if self.__guild.voice_client is not None and self.__guild.voice_client.is_connected() and self.__guild.voice_client.channel != channel:
            await self.__guild.voice_client.disconnect()
        await channel.connect()
        await channel.guild.change_voice_state(
            channel=channel,
            self_deaf=True
        )

    async def play(self, member: nextcord.Member, query: str) -> List[TrackMetadata]:
        with self.__lock:
            self.__check_member_in_voice_channel(member)
            if self.__guild.voice_client is None or not self.__guild.voice_client.is_connected():
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
            self.__guild.voice_client.play(
                self.__audio_source,
                after=self.__on_audio_source_ended
            )

    async def __on_audio_source_ended(self, _):
        self.__safe_switch_to_next_track()
        await self.__safe_start_playing()

    async def next(self, member: nextcord.Member):
        with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_stop_current_track()

    def __safe_stop_current_track(self):
        if self.__guild.voice_client is not None and self.__guild.voice_client.is_playing():
            self.__guild.voice_client.stop()
            self.__audio_source = None

    async def stop(self, member: nextcord.Member):
        with self.__lock:
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
        with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__safe_leave()

    async def __safe_leave(self):
        await self.__safe_stop()
        if self.__guild.voice_client is not None and self.__guild.voice_client.is_connected():
            await self.__guild.voice_client.disconnect()