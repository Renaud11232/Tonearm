import discord
from discord import app_commands


class ZeroIndexTransformer(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: int | None) -> int | None:
        if value is None:
            return None
        return value - 1

    @property
    def min_value(self):
        return 1

    @property
    def type(self):
        return discord.AppCommandOptionType.integer