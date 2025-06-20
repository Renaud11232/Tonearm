import math
from typing import List
import time
import asyncio
import logging

import nextcord
from nextcord.ext import commands

from injector import inject, noninjectable

from tonearm.bot.services.media import MediaService, MediaFetchingException
from tonearm.bot.services.storage import StorageService
from tonearm.configuration import Configuration

from .exceptions import PlayerException
from .audiosource import ControllableFFmpegPCMAudio
from .queue import Queue
from .track import QueuedTrack
from .status import PlayerStatus, AudioSourceStatus


class PlayerService:

    @inject
    @noninjectable("guild", "storage_service")
    def __init__(self, guild: nextcord.Guild, storage_service: StorageService, bot: commands.Bot, queue: Queue, media_service: MediaService, configuration: Configuration):
        self.__guild = guild
        self.__storage_service = storage_service
        self.__bot = bot
        self.__queue = queue
        self.__media_service = media_service
        self.__configuration = configuration
        self.__logger = logging.getLogger("tonearm.player")
        self.__condition = asyncio.Condition()
        self.__audio_source: ControllableFFmpegPCMAudio | None = None
        self.__player_loop_task: asyncio.Task | None = None
        self.__graceful_leave = True
        self.__last_leave = None

    @property
    def __voice_client(self) -> nextcord.VoiceClient | None:
        protocol = nextcord.utils.get(self.__bot.voice_clients, guild=self.__guild)
        if isinstance(protocol, nextcord.VoiceClient):
            return protocol
        if protocol is not None:
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
        if not self.__is_active():
            self.__logger.debug(f"Bot is currently not playing any track in guild {self.__guild.id}")
            raise PlayerException("I'm not currently playing any track")
        self.__logger.debug(f"Bot is currently playing a track in guild {self.__guild.id}")

    def __is_active(self):
        return self.__is_playing() or self.__is_paused()

    def __is_connected(self):
        return self.__voice_client is not None and self.__voice_client.is_connected()

    def __is_playing(self):
        return self.__voice_client is not None and self.__voice_client.is_playing()

    def __is_paused(self):
        return self.__voice_client is not None and self.__voice_client.is_paused()

    def __check_not_in_voice_channel(self):
        self.__logger.debug(f"Checking if the bot is currently connected to a voice channel in the guild {self.__guild.id}")
        if self.__is_connected():
            self.__logger.debug(f"Bot has already joined a voice channel in guild {self.__guild.id}")
            raise PlayerException("I've already joined a voice channel")
        self.__logger.debug(f"Bot hasn't joined a voice channel in guild {self.__guild.id} yet")

    def __check_not_paused(self):
        self.__logger.debug(f"Checking if the audio is currently paused in guild {self.__guild.id}")
        if self.__is_paused():
            self.__logger.debug(f"Audio playback is already paused in guild {self.__guild.id}")
            raise PlayerException("Already paused. No need to rush.")
        self.__logger.debug(f"Audio playback isn't paused in guild {self.__guild.id} yet")

    def __check_paused(self):
        self.__logger.debug(f"Checking if the audio is currently paused in guild {self.__guild.id}")
        if not self.__is_paused():
            self.__logger.debug(f"Audio playback is not paused in guild {self.__guild.id}")
            raise PlayerException("The music never really stopped.")
        self.__logger.debug(f"Audio playback is paused in guild {self.__guild.id}")

    async def __check_queue_not_empty(self):
        self.__logger.debug(f"Checking if the queue is empty in guild {self.__guild.id}")
        if await self.__queue.get_current_track() is None:
            self.__logger.debug(f"Queue is empty in guild {self.__guild.id}")
            raise PlayerException("The queue is empty, what can I do ?")
        self.__logger.debug(f"Queue not empty in guild {self.__guild.id}")

    async def join(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to join him in a voice channel of guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_not_in_voice_channel()
            await self.__safe_join(member.voice.channel)

    async def __safe_join(self, channel: nextcord.VoiceChannel):
        self.__logger.debug(f"Got request to join voice channel {channel.id} of guild {self.__guild.id}")
        self.__logger.debug(f"Checking if the bot was recently kicked from a voice channel in guild {self.__guild.id}")
        if not self.__graceful_leave and self.__last_leave is not None and time.time() < self.__last_leave + 60:
            self.__logger.debug(f"The bot was kicked recently and must wait {math.ceil(self.__last_leave + 60 - time.time())} seconds before joining a voice channel in guild {self.__guild.id}")
            raise PlayerException(f"I can't join right now, please try again in {math.ceil(self.__last_leave + 60 - time.time())} seconds")
        self.__logger.debug(f"The bot wasn't kicked recently, connecting to channel {channel.id} of guild {self.__guild.id}")
        await channel.connect()
        self.__graceful_leave = False
        self.__player_loop_task = asyncio.create_task(self.__player_loop())

    async def __player_loop(self):
        self.__logger.debug(f"Starting player loop for guild {self.__guild.id}")
        try:
            while True:
                async with self.__condition:
                    self.__logger.debug(f"Waiting for the current track to end in guild {self.__guild.id}")
                    while self.__audio_source is not None:
                        await self.__condition.wait()
                while self.__audio_source is None:
                    next_track = await self.__queue.get_next_track()
                    try:
                        stream_url = self.__media_service.fetch(next_track.url)
                        self.__logger.debug(f"Starting playback of url {stream_url} in guild {self.__guild.id}")
                        async with self.__condition:
                            self.__audio_source = ControllableFFmpegPCMAudio(stream_url, buffer_length=self.__configuration.buffer_length)
                            self.__audio_source.volume = await self.__storage_service.get_volume() / 100
                            self.__voice_client.play(
                                self.__audio_source,
                                after=self.__on_audio_source_ended
                            )
                    except asyncio.CancelledError as e:
                        raise e
                    except MediaFetchingException as e:
                        self.__logger.warning(f"Failed to fetch media url in guild {self.__guild.id} : {repr(e)}")
                    except:
                        self.__logger.exception("An unexpected error was raised in the player loop")
        except asyncio.CancelledError:
            self.__logger.debug(f"Cancelled player loop for guild {self.__guild.id}")

    async def __on_audio_source_ended(self, error):
        if error is None:
            self.__logger.debug(f"Audio source ended normally in guild {self.__guild.id}")
        else:
            self.__logger.warning(f"Audio source ended with error in guild {self.__guild.id} : {repr(error)}")
        self.__logger.debug(f"Ending current track and audio source in guild {self.__guild.id}")
        async with self.__condition:
            self.__audio_source = None
            self.__condition.notify()

    async def play(self, member: nextcord.Member, query: str) -> List[QueuedTrack]:
        self.__logger.debug(f"Member {member.id} asked the bot to play {repr(query)} in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            if not self.__is_connected():
                self.__logger.debug(f"The bot is not connected to a voice channel in guild {self.__guild.id}, joining right now")
                await self.__safe_join(member.voice.channel)
            self.__check_same_voice_channel(member)
            tracks = await self.__queue.queue(member, query)
            if len(tracks) == 0:
                self.__logger.debug(f"No tracks found for query {repr(query)} in guild {self.__guild.id}")
                raise PlayerException("No playable track were found")
            return tracks

    def __safe_stop_current_track(self):
        self.__logger.debug(f"Got request to stop the current track playback in guild {self.__guild.id}")
        if self.__voice_client is None:
            self.__logger.debug(f"No voice client found for guild {self.__guild.id}, no need to stop")
        else:
            self.__logger.debug(f"Stopping voice client in guild {self.__guild.id}")
            self.__voice_client.stop()

    async def stop(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to stop playing in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            await self.__safe_stop()

    async def __safe_stop(self, full_clear=False):
        self.__logger.debug(f"Got request to stop playing any track in guild {self.__guild.id}")
        await self.__queue.clear(full=full_clear)
        self.__logger.debug(f"Stopping current track in guild {self.__guild.id}")
        self.__safe_stop_current_track()
        self.__logger.debug(f"Clearing previous tracks in guild {self.__guild.id}")

    async def leave(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to leave the current voice channel in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__safe_leave()

    async def __safe_leave(self):
        self.__logger.debug(f"Got request to leave voice channel in guild {self.__guild.id}")
        self.__graceful_leave = True
        self.__logger.debug(f"Stopping audio playback first in guild {self.__guild.id}")
        await self.__safe_stop(full_clear=True)
        self.__safe_cancel_loop()
        if self.__voice_client is None:
            self.__logger.debug(f"No current voice channel for guild {self.__guild.id}, no need to disconnect")
        else:
            self.__logger.debug(f"Disconnecting voice client in guild {self.__guild.id}")
            await self.__voice_client.disconnect()

    def __safe_cancel_loop(self):
        if self.__player_loop_task is not None:
            self.__player_loop_task.cancel()
            self.__player_loop_task = None

    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        if before.channel != after.channel:
            if before.channel is not None:
                if member.id != self.__bot.user.id:
                    self.__logger.debug(f"Detected that a user moved from (or left) a voice channel in guild {self.__guild.id}")
                    await self.__on_user_moved(before.channel)
                elif after.channel is None:
                    self.__logger.debug(f"Detected that the bot disconnected from its voice channel in guild {self.__guild.id}")
                    await self.__on_bot_disconnected()
                else:
                    self.__logger.debug(f"Detected that the bot was moved to a different voice channel in guild {self.__guild.id}")
                    await self.__on_bot_moved()

    def __is_alone(self, channel: nextcord.VoiceChannel) -> bool:
        others = [m for m in channel.members if m.id != self.__bot.user.id]
        self.__logger.debug(f"Checking if the bot is alone in voice chanel {channel.id} in guild {self.__guild.id} : {len(others) == 0}")
        return len(others) == 0

    async def __on_bot_disconnected(self):
        async with self.__condition:
            if not self.__graceful_leave and self.__voice_client is None:
                self.__logger.warning(f"The bot was kicked from its voice channel in guild {self.__guild.id}, this might cause issues")
                await self.__safe_stop(full_clear=True)
                self.__safe_cancel_loop()
            self.__last_leave = time.time()

    async def __on_bot_moved(self):
        async with self.__condition:
            self.__logger.debug(f"Waiting for the bot to reconnect in guild {self.__guild.id}")
            while not self.__is_connected():
                await asyncio.sleep(0.1)
            self.__logger.debug(f"Finished waiting, leaving voice channel in guild {self.__guild.id}")
            await self.__safe_leave()

    async def __on_user_moved(self, from_channel: nextcord.VoiceChannel):
        async with self.__condition:
            if self.__is_connected() and self.__voice_client.channel == from_channel and self.__is_alone(from_channel):
                self.__logger.debug(f"The bot is now alone in a voice channel in guild {self.__guild.id}, leaving")
                await self.__safe_leave()

    async def debug(self) -> str:
        async with self.__condition:
            return (
                f"self.__audio_source = {repr(self.__audio_source)}\n"
                f"self.__graceful_leave = {repr(self.__graceful_leave)}\n"
                f"self.__last_leave = {repr(self.__last_leave)}\n"
                f"\n"
                f"self.__is_connected() -> {repr(self.__is_connected())}\n"
                f"self.__is_playing() -> {repr(self.__is_playing())}"
            )

    async def clear(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to clear the queue in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__queue.clear()

    async def seek(self, member: nextcord.Member, duration):
        self.__logger.debug(f"Member {member.id} asked the bot to seek to {duration}ms in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_seek(duration)

    def __safe_seek(self, duration: int):
        if self.__is_active():
            self.__logger.debug(f"Bot is currently playing, trying to seek to {duration}ms in guild {self.__guild.id}")
            self.__audio_source.elapsed = duration
        else:
            self.__logger.debug(f"Bot is not currently playing, not seeking in guild {self.__guild.id}")

    async def forward(self, member: nextcord.Member, duration):
        self.__logger.debug(f"Member {member.id} asked the bot to seek forward {duration}ms in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_seek(self.__audio_source.elapsed + duration)

    async def rewind(self, member: nextcord.Member, duration):
        self.__logger.debug(f"Member {member.id} asked the bot to rewind {duration}ms in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__safe_seek(self.__audio_source.elapsed - duration)

    async def now(self, member: nextcord.Member) -> PlayerStatus:
        self.__logger.debug(f"Member {member.id} asked the bot to get the current track in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            return await self.__get_status()

    async def __get_status(self) -> PlayerStatus:
        return PlayerStatus(
            queue=await self.__queue.get_status(),
            audio_source=AudioSourceStatus(
                elapsed=self.__audio_source.elapsed,
                total=self.__audio_source.total,
                volume=await self.__storage_service.get_volume(),
                paused=self.__is_paused(),
            )
        )

    async def queue(self, member: nextcord.Member) -> PlayerStatus:
        self.__logger.debug(f"Member {member.id} asked the bot to get the queue in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__check_queue_not_empty()
            return await self.__get_status()

    async def volume(self, member: nextcord.Member, volume: int):
        self.__logger.debug(f"Member {member.id} asked the bot to change the volume to {volume}% in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            if volume < 0 or volume > 200:
                raise PlayerException("Volume must be between 0 and 200")
            await self.__storage_service.set_volume(volume)
            if self.__is_active():
                self.__audio_source.volume = volume / 100

    async def shuffle(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to shuffle the queue in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__check_queue_not_empty()
            return await self.__queue.shuffle()

    async def pause(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to pause playback in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__check_not_paused()
            self.__voice_client.pause()

    async def resume(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to pause playback in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__check_paused()
            self.__voice_client.resume()

    async def history(self, member: nextcord.Member) -> List[QueuedTrack]:
        self.__logger.debug(f"Member {member.id} asked the bot to get the track history in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            return await self.__queue.get_previous_tracks()

    async def back(self, member: nextcord.Member, position: int = 1):
        self.__logger.debug(f"Member {member.id} asked the bot to go back to track {position} in the history in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__queue.back(position - 1)
            self.__safe_stop_current_track()

    async def jump(self, member: nextcord.Member, position: int = 1):
        self.__logger.debug(f"Member {member.id} asked the bot to jump to track {position} in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            await self.__queue.jump(position - 1)
            self.__safe_stop_current_track()
