from dataclasses import dataclass

from tonearm.bot.services.player.track import QueuedTrack
from tonearm.bot.services.player.loop import LoopMode


@dataclass
class QueueStatus:
    previous_tracks: list[QueuedTrack]
    current_track: QueuedTrack | None
    next_tracks: list[QueuedTrack]
    loop_mode: LoopMode

@dataclass
class AudioSourceStatus:
    elapsed: int
    total: int | float
    volume: int
    paused: bool

@dataclass
class PlayerStatus:
    queue: QueueStatus
    audio_source: AudioSourceStatus