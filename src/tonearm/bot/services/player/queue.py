import asyncio
from typing import List
import logging
import random
from collections import deque

import nextcord

from injector import inject

from tonearm.bot.services.metadata import MetadataService

from .track import QueuedTrack
from .status import QueueStatus
from .exceptions import QueueException


class Queue:

    @inject
    def __init__(self, metadata_service: MetadataService):
        self.__metadata_service = metadata_service
        self.__logger = logging.getLogger("tonearm.queue")
        self.__condition = asyncio.Condition()
        self.__previous_tracks: deque[QueuedTrack] = deque()
        self.__current_track: QueuedTrack | None = None
        self.__next_tracks: deque[QueuedTrack] = deque()

    async def get_next_track(self) -> QueuedTrack:
        self.__logger.debug(f"Getting next track in queue {repr(self)}")
        async with self.__condition:
            if self.__current_track is not None:
                self.__previous_tracks.appendleft(self.__current_track)
                self.__current_track = None
            self.__logger.debug(f"Waiting for next track to be available in queue {repr(self)}")
            while len(self.__next_tracks) == 0:
                await self.__condition.wait()
            self.__current_track = self.__next_tracks.popleft()
            self.__logger.debug(f"Finished waiting, next track in queue {repr(self)} is {repr(self.__current_track)}")
            return self.__current_track

    async def clear(self, full: bool = False):
        async with self.__condition:
            if full:
                self.__logger.debug(f"Completely clearing queue {repr(self)}")
                self.__previous_tracks.clear()
                self.__current_track = None
                self.__next_tracks.clear()
            else:
                self.__logger.debug(f"Clearing next tracks from queue {repr(self)}")
                self.__next_tracks.clear()

    async def queue(self, member: nextcord.Member, query: str):
        self.__logger.debug(f"Fetching track metadata for query {repr(query)} in queue {repr(self)}")
        tracks = [
            QueuedTrack(
                url=track.url,
                title=track.title,
                source=track.source,
                thumbnail=track.thumbnail,
                member=member
            ) for track in self.__metadata_service.fetch(query)
        ]
        async with self.__condition:
            self.__next_tracks.extend(tracks)
            self.__condition.notify()
        self.__logger.debug(f"Added {len(tracks)} track(s) in queue {repr(self)}")
        return tracks

    def __get_previous_tracks(self):
        return list(self.__previous_tracks)

    def __get_current_track(self):
        return self.__current_track

    def __get_next_tracks(self):
        return list(self.__next_tracks)

    async def get_previous_tracks(self) -> List[QueuedTrack]:
        async with self.__condition:
            return self.__get_previous_tracks()

    async def get_current_track(self) -> QueuedTrack | None:
        async with self.__condition:
            return self.__get_current_track()

    async def get_next_tracks(self) -> List[QueuedTrack]:
        async with self.__condition:
            return self.__get_next_tracks()

    async def get_status(self) -> QueueStatus:
        async with self.__condition:
            return QueueStatus(
                previous_tracks=self.__get_previous_tracks(),
                current_track=self.__get_current_track(),
                next_tracks=self.__get_next_tracks(),
            )

    async def shuffle(self):
        self.__logger.debug(f"Shuffling next tracks in queue {repr(self)}")
        async with self.__condition:
            random.shuffle(self.__next_tracks)

    async def jump(self, track: int):
        self.__logger.debug(f"Jumping to track {track} in queue {repr(self)}")
        async with self.__condition:
            if track >= len(self.__next_tracks):
                self.__logger.debug(f"Not enough tracks to jump to track {track} in queue {repr(self)}")
                raise QueueException("Jump failed. That’s outside the queue’s bounds.")
            if self.__current_track is not None:
                self.__previous_tracks.appendleft(self.__current_track)
                self.__current_track = None
            for _ in range(track):
                self.__previous_tracks.appendleft(self.__next_tracks.popleft())
            self.__condition.notify()

    async def back(self, track: int):
        self.__logger.debug(f"Going back to previous track {track} in queue {repr(self)}")
        async with self.__condition:
            if track >= len(self.__previous_tracks):
                self.__logger.debug(f"Not enough tracks in history to go to previous track {track} in queue {repr(self)}")
                raise QueueException(f"That’s further back than my memory goes. Try a smaller number.")
            if self.__current_track is not None:
                self.__next_tracks.appendleft(self.__current_track)
                self.__current_track = None
            for _ in range(track + 1):
                self.__next_tracks.appendleft(self.__previous_tracks.popleft())
            self.__condition.notify()

    async def remove(self, track: int) -> QueuedTrack:
        self.__logger.debug(f"Removing track {track} in queue {repr(self)}")
        async with self.__condition:
            if track >= len(self.__next_tracks):
                self.__logger.debug(f"Not enough tracks to remove track {track} in queue {repr(self)}")
                raise QueueException("Oops ! Nothing to remove at that spot !")
            removed_track = self.__next_tracks[track]
            del self.__next_tracks[track]
            self.__condition.notify()
            return removed_track