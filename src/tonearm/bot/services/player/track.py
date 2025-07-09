from dataclasses import dataclass

import nextcord


@dataclass
class QueuedTrack:
    url: str
    title: str
    source: str
    thumbnail: str | None
    member: nextcord.Member