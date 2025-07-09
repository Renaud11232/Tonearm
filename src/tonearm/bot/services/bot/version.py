from dataclasses import dataclass


@dataclass
class TonearmVersion:
    version: str
    authors: list[str]
    homepage: str
