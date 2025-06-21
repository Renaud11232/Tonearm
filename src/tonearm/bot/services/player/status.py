from collections import namedtuple

QueueStatus = namedtuple("QueueStatus", ["previous_tracks", "current_track", "next_tracks", "loop_mode"])

AudioSourceStatus = namedtuple("AudioSourceStatus", ["elapsed", "total", "volume", "paused"])

PlayerStatus = namedtuple("PlayerStatus", ["queue", "audio_source"])