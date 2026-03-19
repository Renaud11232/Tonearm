import re

import discord
from discord import app_commands

from .exceptions import TranslatableTransformerError


class DurationTransformer(app_commands.Transformer):

    __REGEX = re.compile(r"^(?:([0-9]+)d)?\s*(?:([0-9]+)h)?\s*(?:([0-9]+)m)?\s*(?:([0-9]+)s)?$", re.IGNORECASE)

    async def transform(self, interaction: discord.Interaction, value: str | None) -> int | None:
        if value is None:
            return None
        match = DurationTransformer.__REGEX.search(value)
        if not match:
            raise TranslatableTransformerError(
                value,
                self.type,
                self,
                "`{value}` is not a valid duration.",
                value=value
            )
        groups = match.groups("0")
        days = int(groups[0])
        hours = int(groups[1])
        minutes = int(groups[2])
        seconds = int(groups[3])
        return (seconds + minutes * 60 + hours * 60 * 60 + days * 24 * 60 * 60) * 1_000

    @property
    def type(self):
        return discord.AppCommandOptionType.string