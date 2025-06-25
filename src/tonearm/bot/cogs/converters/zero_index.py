import nextcord
from nextcord import Interaction


class ZeroIndexConverter(nextcord.OptionConverter):

    def __init__(self):
        super().__init__(int)

    async def convert(self, interaction: Interaction, value: int | None) -> int | None:
        if value is None:
            return None
        return value - 1
