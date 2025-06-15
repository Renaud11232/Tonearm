import asyncio
from typing import List
import logging
import random

import nextcord

from injector import inject

from tonearm.bot.services.metadata import MetadataService

from .track import QueuedTrack
from .status import QueueStatus


class Queue:

    @inject
    def __init__(self, metadata_service: MetadataService):
        self.__metadata_service = metadata_service
        self.__logger = logging.getLogger("tonearm.queue")
        self.__condition = asyncio.Condition()
        self.__tracks: List[QueuedTrack] = []
        self.__previous_track = -1
        self.__current_track = None
        self.__next_track = 0

    async def get_next_track(self) -> QueuedTrack:
        self.__logger.debug(f"Getting next track in queue {repr(self)}")
        async with self.__condition:
            self.__previous_track += 1
            self.__current_track = None
            self.__logger.debug(f"Waiting for next track to be available in queue {repr(self)}")
            while self.__next_track >= len(self.__tracks):
                await self.__condition.wait()
            self.__current_track = self.__next_track
            self.__next_track += 1
            track = self.__tracks[self.__current_track]
            self.__logger.debug(f"Finished waiting, next track in queue {repr(self)} is {repr(track)}")
            return track

    async def clear(self, full: bool = False):
        async with self.__condition:
            if full:
                self.__logger.debug(f"Completely clearing queue {repr(self)}")
                self.__previous_track = -1
                self.__current_track = None
                self.__next_track = 0
                self.__tracks.clear()
            else:
                self.__logger.debug(f"Clearing next tracks from queue {repr(self)}")
                self.__tracks[self.__next_track:] = []

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
            self.__tracks.extend(tracks)
            self.__condition.notify()
        self.__logger.debug(f"Added {len(tracks)} track(s) in queue {repr(self)}")
        return tracks

    def __get_previous_tracks(self):
        return list(reversed(self.__tracks[0: self.__previous_track])) if self.__previous_track > -1 else []

    def __get_current_track(self):
        return self.__tracks[self.__current_track] if self.__current_track is not None else None

    def __get_next_tracks(self):
        return self.__tracks[self.__next_track:]

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
            next_tracks = self.__get_next_tracks()
            random.shuffle(next_tracks)
            self.__tracks[self.__next_track:] = next_tracks
