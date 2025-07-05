import nextcord
from nextcord import Interaction, Locale

from tonearm.bot.exceptions import TonearmConverterException
from tonearm.bot.managers import TranslationsManager
from tonearm.bot.services.player import LoopMode


class LoopModeConverter(nextcord.OptionConverter):

    __LOOP_MODE_NAMES = [loop_mode.name for loop_mode in LoopMode]

    def __init__(self):
        super().__init__(str)

    async def convert(self, interaction: Interaction, value: str) -> LoopMode | None:
        if not value:
            return None
        value_upper = value.upper()
        if value_upper not in LoopModeConverter.__LOOP_MODE_NAMES:
            raise TonearmConverterException(
                "`{value}` is not a valid loop mode.",
                value=value
            )
        return LoopMode[value_upper]

    @staticmethod
    def get_choices():
        return {
            TranslationsManager().get(Locale.en_US).gettext("off"): "off",
            TranslationsManager().get(Locale.en_US).gettext("track"): "track",
            TranslationsManager().get(Locale.en_US).gettext("queue"): "queue",
        }

    @staticmethod
    def get_choice_localizations():
        return {
            TranslationsManager().get(Locale.en_US).gettext("off"): {
                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("off"),
                Locale.fr: TranslationsManager().get(Locale.fr).gettext("off")
            },
            TranslationsManager().get(Locale.en_US).gettext("track"): {
                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("track"),
                Locale.fr: TranslationsManager().get(Locale.fr).gettext("track")
            },
            TranslationsManager().get(Locale.en_US).gettext("queue"): {
                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("queue"),
                Locale.fr: TranslationsManager().get(Locale.fr).gettext("queue")
            }
        }
