from dataclasses import dataclass

import nextcord


@dataclass
class Configuration:
    discord_token: str
    log_level: str
    youtube_api_key: str
    max_playlist_length: int
    ffmpeg_executable: str
    youtube_cookies: str | None
    data_path: str
    buffer_length: int
    colour: nextcord.Colour
    status: nextcord.Status
    activity_type: nextcord.ActivityType
    activity_name: str | None
    activity_state: str | None
    activity_url: str | None