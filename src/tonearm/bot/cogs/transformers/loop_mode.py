import discord
from discord import app_commands

from tonearm.bot.services.player import LoopMode

from .exceptions import LoopModeTransformerException


class LoopModeTransformer(app_commands.Transformer):

    async def transform(self, interaction: discord.Interaction, value: str | None) -> LoopMode | None:
        if value is None:
            return None
        if value not in [loop_mode.name for loop_mode in LoopMode]:
            raise LoopModeTransformerException(value, self.type, self)
        return LoopMode[value]

    @property
    def type(self):
        return discord.AppCommandOptionType.string

    @property
    def choices(self):
        return [
            app_commands.Choice(
                name=app_commands.locale_str("off"),
                value=LoopMode.OFF.name
            ),
            app_commands.Choice(
                name=app_commands.locale_str("track"),
                value=LoopMode.TRACK.name
            ),
            app_commands.Choice(
                name=app_commands.locale_str("queue"),
                value=LoopMode.QUEUE.name
            )
        ]