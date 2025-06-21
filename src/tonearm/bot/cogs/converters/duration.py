import re

import nextcord

from tonearm.bot.exceptions import TonearmConverterException


class DurationConverter(nextcord.OptionConverter):

    __REGEX = re.compile(r"^(?:([0-9]+)d)?\s*(?:([0-9]+)h)?\s*(?:([0-9]+)m)?\s*(?:([0-9]+)s)?$")

    async def convert(self, interaction: nextcord.Interaction, argument: str) -> int | None:
        if not argument:
            return None
        match = DurationConverter.__REGEX.search(argument)
        if not match:
            raise TonearmConverterException(f"`{argument}` is not a valid duration.")
        groups = match.groups("0")
        days = int(groups[0])
        hours = int(groups[1])
        minutes = int(groups[2])
        seconds = int(groups[3])
        return (seconds + minutes * 60 + hours * 60 * 60 + days * 24 * 60 * 60) * 1_000
