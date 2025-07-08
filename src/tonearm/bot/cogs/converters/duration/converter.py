import re

import nextcord

from .exceptions import DurationConverterException


class DurationConverter(nextcord.OptionConverter):

    __REGEX = re.compile(r"^(?:([0-9]+)d)?\s*(?:([0-9]+)h)?\s*(?:([0-9]+)m)?\s*(?:([0-9]+)s)?$", re.IGNORECASE)

    def __init__(self):
        super().__init__(str)

    async def convert(self, interaction: nextcord.Interaction, value: str) -> int | None:
        if value is None:
            return None
        match = DurationConverter.__REGEX.search(value)
        if not match:
            raise DurationConverterException(
                "`{value}` is not a valid duration.",
                value=value
            )
        groups = match.groups("0")
        days = int(groups[0])
        hours = int(groups[1])
        minutes = int(groups[2])
        seconds = int(groups[3])
        return (seconds + minutes * 60 + hours * 60 * 60 + days * 24 * 60 * 60) * 1_000
