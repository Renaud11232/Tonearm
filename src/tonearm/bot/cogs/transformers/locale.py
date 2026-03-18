import discord
from discord import app_commands

from .exceptions import LocaleTransformerException


class LocaleTransformer(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: str | None) -> discord.Locale | None:
        if value is None:
            return None
        if value not in [locale.value for locale in discord.Locale]:
            raise LocaleTransformerException(value, self.type, self)
        return discord.Locale(value)

    @property
    def type(self):
        return discord.AppCommandOptionType.string

    @property
    def choices(self):
        return [
            app_commands.Choice(
                name=app_commands.locale_str("American English"),
                value=discord.Locale.american_english.value
            ),
            app_commands.Choice(
                name=app_commands.locale_str("French"),
                value=discord.Locale.french.value
            )
        ]