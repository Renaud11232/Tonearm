import math
from typing import List
import time
import asyncio
import logging

import nextcord
from nextcord.ext import commands

from injector import inject, noninjectable

from tonearm.bot.services.metadata import MetadataService
from tonearm.bot.services.media import MediaService, MediaFetchingException
from tonearm.bot.services.metadata import TrackMetadata

from .exceptions import PlayerException
from .audiosource import ControllableFFmpegPCMAudio


class PlayerService:

    @inject
    @noninjectable("guild")
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
        self.__graceful_leave = True
        self.__last_leave = None

    @property
    def __voice_client(self) -> nextcord.VoiceClient | None:
        protocol = nextcord.utils.get(self.__bot.voice_clients, guild=self.__guild)
        if protocol is None:
            return None
        if isinstance(protocol, nextcord.VoiceClient):
            return protocol
        self.__logger.warning(f"Voice client didn't have the right type (was : {type(protocol).__name__}, expected : VoiceClient), used `None` instead")
        return None

    def __check_member_in_voice_channel(self, member: nextcord.Member):
        self.__logger.debug(f"Checking if member {member.id} of guild {self.__guild.id} is in a voice channel")
        if member.voice is None or member.voice.channel is None:
            self.__logger.debug(f"Member {member.id} of guild {self.__guild.id} was not in a voice channel")
            raise PlayerException("You must join a voice channel first")
        self.__logger.debug(f"Member {member.id} of guild {self.__guild.id} is in a voice channel")

    def __check_same_voice_channel(self, member: nextcord.Member):
        self.__logger.debug(f"Checking if member {member.id} of guild {self.__guild.id} is in the same voice channel as the bot")
        if self.__voice_client is None or member.voice.channel != self.__voice_client.channel:
            self.__logger.debug(f"Member {member.id} of guild {self.__guild.id} was not in the same voice channel as the bot")
            raise PlayerException("I'm not in your voice channel")
        self.__logger.debug(f"Member {member.id} of guild {self.__guild.id} is in the same voice channel as the bot")

    def __check_active_audio_source(self):
        self.__logger.debug(f"Checking if the bot is currently playing a track in the guild {self.__guild.id}")
        if not self.__is_playing():
            self.__logger.debug(f"Bot is currently not playing any track in guild {self.__guild.id}")
            raise PlayerException("I'm not currently playing any track")
        self.__logger.debug(f"Bot is currently playing a track in guild {self.__guild.id}")

    def __is_connected(self):
        return self.__voice_client is not None and self.__voice_client.is_connected()

    def __is_playing(self):
        return self.__voice_client is not None and self.__voice_client.is_playing()

    def __check_not_in_voice_channel(self):
        self.__logger.debug(f"Checking if the bot is currently connected to a voice channel in the guild {self.__guild.id}")
        if self.__is_connected():
            self.__logger.debug(f"Bot has already joined a voice channel in guild {self.__guild.id}")
            raise PlayerException("I've already joined a voice channel")
        self.__logger.debug(f"Bot hasn't joined a voice channel in guild {self.__guild.id} yet")

    async def join(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to join him in a voice channel of guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_not_in_voice_channel()
            await self.__safe_join(member.voice.channel)

    async def __safe_join(self, channel: nextcord.VoiceChannel):
        self.__logger.debug(f"Got request to join voice channel {channel.id} of guild {self.__guild.id}")
        self.__logger.debug(f"Checking if the bot was recently kicked from a voice channel in guild {self.__guild.id}")
        if not self.__graceful_leave and  self.__last_leave is not None and time.time() < self.__last_leave + 60:
            self.__logger.debug(f"The bot was kicked recently and must wait {math.floor(self.__last_leave + 60 - time.time())} seconds before joining a voice channel in guild {self.__guild.id}")
            raise PlayerException(f"I can't join right now, please try again in {math.floor(self.__last_leave + 60 - time.time())} seconds")
        self.__logger.debug(f"The bot wasn't kicked recently, connecting to channel {channel.id} of guild {self.__guild.id}")
        await channel.connect()
        self.__graceful_leave = False

    async def play(self, member: nextcord.Member, query: str) -> List[TrackMetadata]:
        self.__logger.debug(f"Member {member.id} asked the bot to play {repr(query)} in guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            if not self.__is_connected():
                self.__logger.debug(f"The bot is not connected to a voice channel in guild {self.__guild.id}, joining right now")
                await self.__safe_join(member.voice.channel)
            self.__check_same_voice_channel(member)
            self.__logger.debug(f"Fetching track metadata for query {repr(query)} in guild {self.__guild.id}")
            tracks = await self.__metadata_service.fetch(query)
            if len(tracks) == 0:
                self.__logger.debug(f"No tracks found for query {repr(query)} in guild {self.__guild.id}")
                raise PlayerException("No playable track were found")
            self.__logger.debug(f"Queuing {len(tracks)} matching tracks for query {repr(query)} in guild {self.__guild.id}")
            self.__next_tracks.extend(tracks)
            self.__logger.debug(f"Checking if a track is currently playing in guild {self.__guild.id}")
            if self.__current_track is None:
                self.__logger.debug(f"No track currently playing, switching to the next track in queue for guild {self.__guild.id}")
                self.__safe_switch_to_next_track()
                self.__logger.debug(f"Starting playback of track in guild {self.__guild.id}")
                await self.__safe_start_playing()
            return tracks

    def __safe_switch_to_next_track(self):
        if self.__current_track is not None and not self.__stopped:
            self.__logger.debug(f"Moving current track to previous tracks in guild {self.__guild.id}")
            self.__previous_tracks.append(self.__current_track)
        if len(self.__next_tracks) == 0:
            self.__logger.debug(f"No other tracks in the queue in guild {self.__guild.id}")
            self.__current_track = None
        else:
            self.__logger.debug(f"Next track from the queue selected in guild {self.__guild.id}")
            self.__current_track = self.__next_tracks.pop(0)
        self.__logger.debug(f"Current track is now {self.__current_track} in guild {self.__guild.id}")

    async def __safe_start_playing(self):
        self.__logger.debug(f"Got request to start playing track in guild {self.__guild.id}")
        if self.__current_track is not None:
            self.__stopped = False
            self.__logger.debug(f"Fetching media stream url from media_service in guild {self.__guild.id}")
            try:
                stream_url = await self.__media_service.fetch(self.__current_track.url)
                self.__logger.debug(f"Creating audio source from url {repr(stream_url)} in guild {self.__guild.id}")
                self.__audio_source = ControllableFFmpegPCMAudio(stream_url)
                self.__logger.debug(f"Starting track playback in guild {self.__guild.id}")
                self.__voice_client.play(
                    self.__audio_source,
                    after=self.__on_audio_source_ended
                )
            except MediaFetchingException as e:
                self.__logger.warning(f"Failed to start playing track {repr(self.__current_track)} in guild {self.__guild.id} : {repr(e)}")
                self.__current_track = None
                raise e
        else:
            self.__logger.debug(f"No track currently selected in guild {self.__guild.id}, did not start playing")

    async def __on_audio_source_ended(self, error):
        if error is None:
            self.__logger.debug(f"Audio source ended normally in guild {self.__guild.id}")
        else:
            self.__logger.warning(f"Audio source ended with error in guild {self.__guild.id} : {repr(error)}")
        self.__logger.debug(f"Ending current track and audio source in guild {self.__guild.id}")
        self.__audio_source = None
        self.__safe_switch_to_next_track()
        while self.__current_track is not None:
            try:
                await self.__safe_start_playing()
                break
            except MediaFetchingException:
                self.__safe_switch_to_next_track()

    async def next(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to skip the current track in guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_stop_current_track()

    def __safe_stop_current_track(self):
        self.__logger.debug(f"Got request to stop the current track playback in guild {self.__guild.id}")
        if self.__voice_client is None:
            self.__logger.debug(f"No voice client found for guild {self.__guild.id}, no need to stop")
        else:
            self.__logger.debug(f"Stopping voice client in guild {self.__guild.id}")
            self.__voice_client.stop()

    async def stop(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to stop playing in guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            await self.__safe_stop()

    async def __safe_stop(self):
        self.__logger.debug(f"Got request to stop playing any track in guild {self.__guild.id}")
        self.__stopped = True
        self.__safe_clear()
        self.__logger.debug(f"Stopping current track in guild {self.__guild.id}")
        self.__safe_stop_current_track()
        self.__logger.debug(f"Clearing previous tracks in guild {self.__guild.id}")
        self.__previous_tracks.clear()

    async def leave(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to leave the current voice channel in guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__safe_leave()

    async def __safe_leave(self):
        self.__logger.debug(f"Got request to leave voice channel in guild {self.__guild.id}")
        self.__graceful_leave = True
        self.__logger.debug(f"Stopping audio playback first in guild {self.__guild.id}")
        await self.__safe_stop()
        if self.__voice_client is None:
            self.__logger.debug(f"No current voice channel for guild {self.__guild.id}, no need to disconnect")
        else:
            self.__logger.debug(f"Disconnecting voice client in guild {self.__guild.id}")
            await self.__voice_client.disconnect()

    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        if before.channel != after.channel:
            if before.channel is not None:
                if member.id != self.__bot.user.id:
                    self.__logger.debug(f"Detected that a user moved from (or left) a voice channel in guild {self.__guild.id}")
                    await self.__on_user_moved(before.channel)
                elif after.channel is None:
                    self.__logger.warning(f"Detected that the bot was kicked from its voice channel in guild {self.__guild.id}, this might cause issues")
                    await self.__on_bot_disconnected()
                else:
                    self.__logger.debug(f"Detected that the bot was moved to a different voice channel in guild {self.__guild.id}")
                    await self.__on_bot_moved()

    def __is_alone(self, channel: nextcord.VoiceChannel) -> bool:
        others = [m for m in channel.members if m.id != self.__bot.user.id]
        self.__logger.debug(f"Checking if the bot is alone in voice chanel {channel.id} in guild {self.__guild.id} : {len(others) == 0}")
        return len(others) == 0

    async def __on_bot_disconnected(self):
        await self.__safe_stop()
        self.__last_leave = time.time()

    async def __on_bot_moved(self):
        async with self.__lock:
            self.__logger.debug(f"Waiting for the bot to reconnect in guild {self.__guild.id} before leaving on its own")
            while not self.__is_connected():
                await asyncio.sleep(0.1)
            self.__logger.debug(f"Finished waiting, leaving voice channel in guild {self.__guild.id}")
            await self.__safe_leave()

    async def __on_user_moved(self, from_channel: nextcord.VoiceChannel):
        async with self.__lock:
            if self.__is_connected() and self.__voice_client.channel == from_channel and self.__is_alone(from_channel):
                self.__logger.debug(f"The bot is now alone in a voice channel in guild {self.__guild.id}, leaving")
                await self.__safe_leave()

    async def debug(self) -> str:
        async with self.__lock:
            return (
                f"self.__previous_tracks = {repr(self.__previous_tracks)}\n"
                f"self.__current_track = {repr(self.__current_track)}\n"
                f"self.__next_tracks = {repr(self.__next_tracks)}\n"
                f"self.__audio_source = {repr(self.__audio_source)}\n"
                f"self.__stopped = {repr(self.__stopped)}\n"
                f"self.__graceful_leave = {repr(self.__graceful_leave)}\n"
                f"self.__last_leave = {repr(self.__last_leave)}\n"
                f"\n"
                f"self.__is_connected() -> {repr(self.__is_connected())}\n"
                f"self.__is_playing() -> {repr(self.__is_playing())}"
            )

    async def clear(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to clear the queue in guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__safe_clear()

    def __safe_clear(self):
        self.__logger.debug(f"Clearing queue in guild {self.__guild.id}")
        self.__next_tracks.clear()

    async def seek(self, member: nextcord.Member, duration):
        self.__logger.debug(f"Member {member.id} asked the bot to seek to {duration}ms in guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_seek(duration)

    def __safe_seek(self, duration: int):
        if self.__is_playing():
            self.__logger.debug(f"Bot is currently playing, trying to seek to {duration}ms in guild {self.__guild.id}")
            self.__audio_source.elapsed = duration
        else:
            self.__logger.debug(f"Bot is not currently playing, not seeking in guild {self.__guild.id}")

    async def forward(self, member: nextcord.Member, duration):
        self.__logger.debug(f"Member {member.id} asked the bot to seek forward {duration}ms in guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_seek(self.__audio_source.elapsed + duration)

    async def rewind(self, member: nextcord.Member, duration):
        self.__logger.debug(f"Member {member.id} asked the bot to rewind {duration}ms in guild {self.__guild.id}")
        async with self.__lock:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_seek(self.__audio_source.elapsed - duration)