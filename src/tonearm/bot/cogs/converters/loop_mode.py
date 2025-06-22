import nextcord
from nextcord import Interaction

from tonearm.bot.exceptions import TonearmConverterException
from tonearm.bot.services.player import LoopMode


class LoopModeConverter(nextcord.OptionConverter):

    async def convert(self, interaction: Interaction, value: str) -> LoopMode | None:
        if not value:
            return None
        if value.upper() not in LoopMode._member_names_:
            raise TonearmConverterException(f"`{value}` is not a valid loop mode.")
        return LoopMode[value.upper()]