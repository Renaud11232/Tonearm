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
        self.__next_track = 0

    async def get_next_track(self) -> QueuedTrack:
        self.__logger.debug(f"Getting next track in queue {repr(self)}")
        async with self.__condition:
            self.__logger.debug(f"Waiting for next track to be available in queue {repr(self)}")
            while self.__next_track >= len(self.__tracks):
                await self.__condition.wait()
            track = self.__tracks[self.__next_track]
            self.__logger.debug(f"Finished waiting, next track in queue {repr(self)} is {repr(track)}")
            self.__next_track += 1
            return track

    async def clear(self):
        self.__logger.debug(f"Clearing queue {repr(self)}")
        async with self.__condition:
            self.__next_track = 0
            self.__tracks.clear()

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
        return self.__tracks[0: self.__next_track - 1] if self.__next_track > 1 else []

    def __get_current_track(self):
        return self.__tracks[self.__next_track - 1] if self.__next_track > 0 else None

    def __get_next_tracks(self):
        return self.__tracks[self.__next_track:]

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
