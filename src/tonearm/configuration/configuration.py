from dataclasses import dataclass

import discord


@dataclass
class Configuration:
    discord_token: str
    log_level: int
    youtube_api_key: str
    max_playlist_length: int
    ffmpeg_executable: str
    youtube_cookies: str | None
    data_path: str
    buffer_length: int
    colour: discord.Colour
    status: discord.Status
    activity_type: discord.ActivityType
    activity_name: str | None
    activity_state: str | None
    activity_url: str | None
    deno_executable: str