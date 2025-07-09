from dataclasses import dataclass

import nextcord


@dataclass
class Configuration:
    discord_token: str
    log_level: str
    youtube_api_key: str
    cobalt_api_url: str
    cobalt_api_key: str | None
    data_path: str
    buffer_length: int
    colour: nextcord.Colour