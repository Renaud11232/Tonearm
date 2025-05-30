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

    def __init__(self, bot: commands.Bot, metadata_service: MetadataService, media_service: MediaService):
        self.__bot = bot
        self.__metadata_service = metadata_service
        self.__media_service = media_service
        self.__lock = threading.Lock()
        self.__previous_tracks = []
        self.__current_track = None
        self.__next_tracks = []
        self.__voice_channel = None
        self.__voice_client = None
        self.__audio_source = None

    @staticmethod
    def __check_member_in_voice_channel(voice: nextcord.VoiceState):
        if voice is None or voice.channel is None:
            raise TonearmException("You must join a voice channel first")

    def __check_same_voice_channel(self, voice: nextcord.VoiceState):
        if self.__voice_channel != voice.channel.id:
            raise TonearmException("I'm not in your voice channel")

    def __check_active_audio_source(self):
        if self.__audio_source is None:
            raise TonearmException("I'm not currently playing any track")

    def __check_not_in_voice_channel(self):
        if self.__voice_channel is not None:
            raise TonearmException("I've already joined a voice channel")

    async def join(self, voice: nextcord.VoiceState):
        with self.__lock:
            self.__check_member_in_voice_channel(voice)
            await self.__join(voice)

    async def __join(self, voice: nextcord.VoiceState):
        self.__check_not_in_voice_channel()
        self.__voice_client = await voice.channel.connect()
        await voice.channel.guild.change_voice_state(
            channel=voice.channel,
            self_deaf=True
        )
        self.__voice_channel = voice.channel.id

    async def leave(self, voice: nextcord.VoiceState):
        with self.__lock:
            self.__check_member_in_voice_channel(voice)
            self.__check_same_voice_channel(voice)
            if self.__audio_source is not None:
                await self.__stop()
            await self.__voice_client.disconnect()
            self.__voice_channel = None
            self.__voice_client = None

    async def play(self, voice: nextcord.VoiceState, query: str) -> List[TrackMetadata]:
        with self.__lock:
            self.__check_member_in_voice_channel(voice)
            if self.__voice_channel is None:
                await self.__join(voice)
            self.__check_same_voice_channel(voice)
            tracks = await self.__metadata_service.fetch(query)
            if len(tracks) == 0:
                raise TonearmException("No playable track were found")
            self.__next_tracks.extend(tracks)
            if self.__current_track is None:
                await self.__start_next_track()
            return tracks

    async def stop(self, voice: nextcord.VoiceState):
        with self.__lock:
            self.__check_member_in_voice_channel(voice)
            self.__check_same_voice_channel(voice)
            self.__check_active_audio_source()
            await self.__stop()

    async def __stop(self):
        self.__voice_client.stop()
        self.__end_current_track()
        self.__previous_tracks.clear()
        self.__next_tracks.clear()

    async def __start_next_track(self):
        self.__current_track = self.__next_tracks.pop(0)
        stream_url = await self.__media_service.fetch(self.__current_track.url)
        self.__audio_source = ControllableFFmpegPCMAudio(stream_url)
        self.__voice_client.play(
            self.__audio_source,
            after=self.__on_audio_source_ended
        )

    async def __on_audio_source_ended(self, _):
        self.__end_current_track()
        if len(self.__next_tracks) > 0:
            await self.__start_next_track()

    def __end_current_track(self):
        self.__audio_source = None
        self.__previous_tracks.append(self.__current_track)
        self.__current_track = None

    async def next(self, voice: nextcord.VoiceState):
        with self.__lock:
            self.__check_member_in_voice_channel(voice)
            self.__check_same_voice_channel(voice)
            self.__check_active_audio_source()
            self.__voice_client.stop()