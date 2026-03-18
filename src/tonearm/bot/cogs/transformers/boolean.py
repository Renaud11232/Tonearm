import discord
from discord import app_commands

from .exceptions import BooleanTransformerException


class BooleanTransformer(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: str | None) -> bool | None:
        if value is None:
            return None
        if value.upper() == "TRUE":
            return True
        if value.upper() == "FALSE":
            return False
        raise BooleanTransformerException(
            "`{value}` is not a valid boolean value.",
            value=value
        )

    @property
    def type(self):
        return discord.AppCommandOptionType.string

    @property
    def choices(self):
        return [
            app_commands.Choice(
                name=app_commands.locale_str("True"),
                value="TRUE"
            ),
            app_commands.Choice(
                name=app_commands.locale_str("False"),
                value="FALSE"
            )
        ]