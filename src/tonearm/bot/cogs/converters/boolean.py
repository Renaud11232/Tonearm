import nextcord
from nextcord import Interaction

from tonearm.bot.exceptions import TonearmConverterException


class BooleanConverter(nextcord.OptionConverter):

    def __init__(self):
        super().__init__(str)

    async def convert(self, interaction: Interaction, value: str) -> None | bool:
        if value is None:
            return None
        if value.upper() == "TRUE":
            return True
        if value.upper() == "FALSE":
            return False
        raise TonearmConverterException(f"`{value}` is not a valid boolean value.")