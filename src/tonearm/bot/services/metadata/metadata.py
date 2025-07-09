from dataclasses import dataclass


@dataclass
class TrackMetadata:
    url: str
    title: str
    source: str
    thumbnail: str | None
