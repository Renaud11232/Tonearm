from dataclasses import dataclass

import discord


@dataclass
class QueuedTrack:
    url: str
    title: str
    source: str
    thumbnail: str | None
    member: discord.Member