import math
from typing import List
import time
import asyncio
import logging

import nextcord
from nextcord.ext import commands

from injector import inject, noninjectable

from tonearm.bot.services.source import SourceService, SourceOpeningException
from tonearm.bot.services.storage import StorageService
from tonearm.bot.services.embed import EmbedService

from .exceptions import PlayerException
from .audiosource import ControllableFFmpegPCMAudio
from .queue import Queue
from .track import QueuedTrack
from .status import PlayerStatus, AudioSourceStatus
from .loop import LoopMode
from .voice_client import TonearmVoiceClient
from .vote import VoteStatus


class PlayerService:

    @inject
    @noninjectable("guild", "storage_service", "embed_service")
    def __init__(self,
                 guild: nextcord.Guild,
                 storage_service: StorageService,
                 embed_service: EmbedService,
                 bot: commands.Bot,
                 queue: Queue,
                 source_service: SourceService):
        self.__guild = guild
        self.__storage_service = storage_service
        self.__embed_service = embed_service
        self.__bot = bot
        self.__queue = queue
        self.__source_service = source_service
        self.__logger = logging.getLogger("tonearm.player")
        self.__condition = asyncio.Condition()
        self.__audio_source: ControllableFFmpegPCMAudio | None = None
        self.__player_loop_task: asyncio.Task | None = None
        self.__last_forced_leave: float | None = None
        self.__votes = set()

    @property
    def __voice_client(self) -> TonearmVoiceClient | None:
        protocol = nextcord.utils.get(self.__bot.voice_clients, guild=self.__guild)
        if isinstance(protocol, TonearmVoiceClient):
            return protocol
        return None

    def __check_member_in_voice_channel(self, member: nextcord.Member):
        self.__logger.debug(f"Checking if member {member.id} of guild {self.__guild.id} is in a voice channel")
        if member.voice is None or member.voice.channel is None:
            self.__logger.debug(f"Member {member.id} of guild {self.__guild.id} was not in a voice channel")
            raise PlayerException(
                "You must join a voice channel first."
            )
        self.__logger.debug(f"Member {member.id} of guild {self.__guild.id} is in a voice channel")

    def __check_same_voice_channel(self, member: nextcord.Member):
        self.__logger.debug(f"Checking if member {member.id} of guild {self.__guild.id} is in the same voice channel as the bot")
        if self.__voice_client is None or member.voice.channel != self.__voice_client.channel:
            self.__logger.debug(f"Member {member.id} of guild {self.__guild.id} was not in the same voice channel as the bot")
            raise PlayerException(
                "I'm not in the same voice channel !"
            )
        self.__logger.debug(f"Member {member.id} of guild {self.__guild.id} is in the same voice channel as the bot")

    def __check_active_audio_source(self):
        self.__logger.debug(f"Checking if the bot is currently playing a track in the guild {self.__guild.id}")
        if not self.__is_active():
            self.__logger.debug(f"Bot is currently not playing any track in guild {self.__guild.id}")
            raise PlayerException(
                "I'm not currently playing any track."
            )
        self.__logger.debug(f"Bot is currently playing a track in guild {self.__guild.id}")

    def __check_not_in_voice_channel(self):
        self.__logger.debug(f"Checking if the bot is currently connected to a voice channel in the guild {self.__guild.id}")
        if self.__is_connected():
            self.__logger.debug(f"Bot has already joined a voice channel in guild {self.__guild.id}")
            raise PlayerException(
                "I've already joined a voice channel."
            )
        self.__logger.debug(f"Bot hasn't joined a voice channel in guild {self.__guild.id} yet")

    def __check_not_paused(self):
        self.__logger.debug(f"Checking if the audio is currently paused in guild {self.__guild.id}")
        if self.__is_paused():
            self.__logger.debug(f"Audio playback is already paused in guild {self.__guild.id}")
            raise PlayerException(
                "Already paused. No need to rush."
            )
        self.__logger.debug(f"Audio playback isn't paused in guild {self.__guild.id} yet")

    def __check_paused(self):
        self.__logger.debug(f"Checking if the audio is currently paused in guild {self.__guild.id}")
        if not self.__is_paused():
            self.__logger.debug(f"Audio playback is not paused in guild {self.__guild.id}")
            raise PlayerException(
                "The music never really stopped."
            )
        self.__logger.debug(f"Audio playback is paused in guild {self.__guild.id}")

    def __check_queue_not_empty(self):
        self.__logger.debug(f"Checking if the queue is empty in guild {self.__guild.id}")
        if self.__queue.get_current_track() is None:
            self.__logger.debug(f"Queue is empty in guild {self.__guild.id}")
            raise PlayerException(
                "The queue is empty, what can I do ?"
            )
        self.__logger.debug(f"Queue not empty in guild {self.__guild.id}")

    def __check_history_not_empty(self):
        self.__logger.debug(f"Checking if the history is empty in guild {self.__guild.id}")
        if len(self.__queue.get_previous_tracks()) == 0:
            self.__logger.debug(f"History is empty in guild {self.__guild.id}")
            raise PlayerException(
                "I can't do that with no track in the history."
            )
        self.__logger.debug(f"History not empty in guild {self.__guild.id}")

    def __check_not_kicked_recently(self):
        self.__logger.debug(f"Checking if the bot was recently kicked from a voice channel in guild {self.__guild.id}")
        if self.__last_forced_leave is not None and time.time() < self.__last_forced_leave + 60:
            remaining_seconds = math.ceil(self.__last_forced_leave + 60 - time.time())
            self.__logger.debug(f"The bot was kicked recently and must wait {remaining_seconds} seconds before joining a voice channel in guild {self.__guild.id}")
            raise PlayerException(
                "I got abruptly disconnected, ask me again in {remaining_seconds} second(s).",
                remaining_seconds=math.ceil(self.__last_forced_leave + 60 - time.time())
            )
        self.__logger.debug(f"The bot wasn't kicked recently")

    def __check_did_not_vote_yet(self, member: nextcord.Member):
        self.__logger.debug(f"Checking the member {member.id} did already vote to skip the current track in guild {self.__guild.id}")
        if member.id in self.__votes:
            self.__logger.debug(f"Member {member.id} already did already vote in guild {self.__guild.id}")
            raise PlayerException(
                "You already voted to skip this track."
            )
        self.__logger.debug(f"Member {member.id} did not already vote in guild {self.__guild.id}")

    def __is_active(self):
        return self.__is_playing() or self.__is_paused()

    def __is_connected(self):
        return self.__voice_client is not None and self.__voice_client.is_connected()

    def __is_playing(self):
        return self.__voice_client is not None and self.__voice_client.is_playing()

    def __is_paused(self):
        return self.__voice_client is not None and self.__voice_client.is_paused()

    async def join(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to join him in a voice channel of guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_not_in_voice_channel()
            await self.__safe_join(member.voice.channel)

    async def __safe_join(self, channel: nextcord.VoiceChannel):
        self.__logger.debug(f"Got request to join voice channel {channel.id} of guild {self.__guild.id}")
        self.__check_not_kicked_recently()
        await channel.connect(cls=TonearmVoiceClient)
        self.__voice_client.add_listener("disconnect", self.__on_disconnect)
        await self.__queue.loop(LoopMode.OFF)
        self.__player_loop_task = asyncio.create_task(self.__player_loop())

    async def __on_disconnect(self, force: bool):
        self.__logger.debug(f"Voice client disconnected in guild {self.__guild.id}")
        if force:
            self.__logger.warning(f"Forced to disconnect from voice channel in guild {self.__guild.id}, this can cause some issues")
            self.__last_forced_leave = time.time()
        else:
            self.__logger.debug(f"Gracefully disconnected from voice channel in guild {self.__guild.id}")
            self.__last_forced_leave = None
        await self.__safe_stop(full_clear=True)
        self.__safe_cancel_loop()

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
                    self.__logger.debug(f"Starting playback of url {next_track.url} in guild {self.__guild.id}")
                    try:
                        async with self.__condition:
                            self.__audio_source = self.__source_service.open(next_track.url)
                            self.__audio_source.volume = self.__storage_service.get_volume() / 100
                            self.__voice_client.play(
                                self.__audio_source,
                                after=self.__on_audio_source_ended
                            )
                            if self.__storage_service.get_announcements():
                                await self.__send_to_channel(self.__embed_service.now(self.__get_status()))
                    except asyncio.CancelledError as e:
                        raise e
                    except SourceOpeningException as e:
                        self.__logger.warning(f"Failed to fetch media url in guild {self.__guild.id} : {repr(e)}")
                        await self.__send_to_channel(self.__embed_service.error(e))
                    except:
                        self.__logger.exception("An unexpected error was raised in the player loop :")
                        await self.__send_to_channel(self.__embed_service.error_message(
                            "I faced an unexpected error, please contact {owner}. I feel weird.",
                            owner=(await self.__bot.application_info()).owner.mention
                        ))
        except asyncio.CancelledError:
            self.__logger.debug(f"Cancelled player loop for guild {self.__guild.id}")

    async def __send_to_channel(self, embed: nextcord.Embed):
        channel = self.__storage_service.get_channel()
        self.__logger.debug(f"Sending message to the configured bot channel ({channel.id}) : in guild {self.__guild.id}")
        if channel is not None:
            await channel.send(
                embed=embed
            )
        else:
            self.__logger.debug(f"No channel configured for guild {self.__guild.id}")

    async def __on_audio_source_ended(self, error):
        if error is None:
            self.__logger.debug(f"Audio source ended normally in guild {self.__guild.id}")
        else:
            self.__logger.warning(f"Audio source ended with error in guild {self.__guild.id} : {repr(error)}")
        self.__logger.debug(f"Ending current track and audio source in guild {self.__guild.id}, resetting votes")
        async with self.__condition:
            self.__audio_source = None
            self.__condition.notify()
            self.__votes.clear()

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
                raise PlayerException(
                    "No playable track were found !"
                )
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
        self.__queue.clear(full=full_clear)
        await self.__queue.loop(LoopMode.OFF)
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
                    await self.__on_user_moved_or_left(member, before.channel)
                elif after.channel is not None:
                    self.__logger.debug(f"Detected that the bot was moved to a different voice channel in guild {self.__guild.id}")
                    await self.__on_bot_moved()

    def __is_alone(self) -> bool:
        others = self.__get_humans_in_same_voice_channel()
        self.__logger.debug(f"Checking if the bot is alone in voice chanel in guild {self.__guild.id} : {len(others) == 0}")
        return len(others) == 0

    def __get_humans_in_same_voice_channel(self):
        return [member for member in self.__voice_client.channel.members if not member.bot]

    async def __on_bot_moved(self):
        async with self.__condition:
            self.__logger.debug(f"Waiting for the bot to reconnect in guild {self.__guild.id}")
            while not self.__is_connected():
                await asyncio.sleep(0.1)
            self.__logger.debug(f"Finished waiting, leaving voice channel in guild {self.__guild.id}")
            await self.__safe_leave()

    async def __on_user_moved_or_left(self, member: nextcord.Member, from_channel: nextcord.VoiceChannel):
        async with self.__condition:
            if self.__is_connected() and self.__voice_client.channel == from_channel:
                if self.__is_alone():
                    self.__logger.debug(f"The bot is now alone in a voice channel in guild {self.__guild.id}, leaving")
                    await self.__safe_leave()
                else:
                    self.__votes.discard(member.id)
                    await self.__safe_handle_vote(True)

    def clear(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to clear the queue in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__queue.clear()

    def seek(self, member: nextcord.Member, duration: int):
        self.__logger.debug(f"Member {member.id} asked the bot to seek to {duration}ms in guild {self.__guild.id}")
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

    def forward(self, member: nextcord.Member, duration: int):
        self.__logger.debug(f"Member {member.id} asked the bot to seek forward {duration}ms in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__check_active_audio_source()
        self.__safe_seek(self.__audio_source.elapsed + duration)

    def rewind(self, member: nextcord.Member, duration: int):
        self.__logger.debug(f"Member {member.id} asked the bot to rewind {duration}ms in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__check_active_audio_source()
        self.__safe_seek(self.__audio_source.elapsed - duration)

    def now(self, member: nextcord.Member) -> PlayerStatus:
        self.__logger.debug(f"Member {member.id} asked the bot to get the current track in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__check_active_audio_source()
        return self.__get_status()

    def __get_status(self) -> PlayerStatus:
        return PlayerStatus(
            queue=self.__queue.get_status(),
            audio_source=AudioSourceStatus(
                elapsed=self.__audio_source.elapsed,
                total=self.__audio_source.total,
                volume=self.__storage_service.get_volume(),
                paused=self.__is_paused(),
            )
        )

    def queue(self, member: nextcord.Member) -> PlayerStatus:
        self.__logger.debug(f"Member {member.id} asked the bot to get the queue in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__check_queue_not_empty()
        return self.__get_status()

    def volume(self, member: nextcord.Member, volume: int):
        self.__logger.debug(f"Member {member.id} asked the bot to change the volume to {volume}% in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__storage_service.set_volume(volume)
        if self.__is_active():
            self.__audio_source.volume = volume / 100

    def shuffle(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to shuffle the queue in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__check_queue_not_empty()
        self.__queue.shuffle()

    def pause(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to pause playback in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__check_active_audio_source()
        self.__check_not_paused()
        self.__voice_client.pause()

    def resume(self, member: nextcord.Member):
        self.__logger.debug(f"Member {member.id} asked the bot to pause playback in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        self.__check_active_audio_source()
        self.__check_paused()
        self.__voice_client.resume()

    def history(self, member: nextcord.Member) -> List[QueuedTrack]:
        self.__logger.debug(f"Member {member.id} asked the bot to get the track history in guild {self.__guild.id}")
        self.__check_member_in_voice_channel(member)
        self.__check_same_voice_channel(member)
        return self.__queue.get_previous_tracks()

    async def back(self, member: nextcord.Member, track: int):
        self.__logger.debug(f"Member {member.id} asked the bot to go back to track {track} in the history in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_history_not_empty()
            await self.__queue.back(track)
            self.__safe_stop_current_track()

    async def jump(self, member: nextcord.Member, track: int):
        self.__logger.debug(f"Member {member.id} asked the bot to jump to track {track} in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            await self.__safe_jump(track)

    async def __safe_jump(self, track: int):
        await self.__queue.jump(track)
        self.__safe_stop_current_track()

    async def remove(self, member: nextcord.Member, track: int) -> QueuedTrack:
        self.__logger.debug(f"Member {member.id} asked the bot to remove track {track} from the queue in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_queue_not_empty()
            return await self.__queue.remove(track)

    async def move(self, member: nextcord.Member, from_: int, to: int) -> QueuedTrack:
        self.__logger.debug(f"Member {member.id} asked the bot to move track {from_} to {to} in in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_queue_not_empty()
            return await self.__queue.move(from_, to)

    async def loop(self, member: nextcord.Member, mode: LoopMode):
        self.__logger.debug(f"Member {member.id} asked the bot to change the loop mode to {mode} in in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            await self.__queue.loop(mode)

    async def votenext(self, member: nextcord.Member) -> VoteStatus:
        self.__logger.debug(f"Member {member.id} voted to skip the current track in guild {self.__guild.id}")
        async with self.__condition:
            self.__check_member_in_voice_channel(member)
            self.__check_same_voice_channel(member)
            self.__check_active_audio_source()
            self.__check_did_not_vote_yet(member)
            self.__votes.add(member.id)
            return await self.__safe_handle_vote()

    async def __safe_handle_vote(self, should_announce: bool = False):
        required_votes = math.ceil(len(self.__get_humans_in_same_voice_channel()) / 2)
        received_votes = len(self.__votes)
        status = VoteStatus(
            required_votes=required_votes,
            received_votes=received_votes,
            needed_votes=required_votes - received_votes,
        )
        self.__logger.debug(f"Received {status.received_votes} votes out of {status.required_votes} votes required in guild {self.__guild.id}")
        if status.received_votes > 0 and status.received_votes >= status.required_votes:
            await self.__safe_jump(0)
            if should_announce:
                await self.__send_to_channel(self.__embed_service.votenext(status))
        return status
