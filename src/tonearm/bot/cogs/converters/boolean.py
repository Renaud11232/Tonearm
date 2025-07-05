import nextcord
from nextcord import Interaction, Locale

from tonearm.bot.exceptions import TonearmConverterException
from tonearm.bot.managers import TranslationsManager


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
        raise TonearmConverterException(
            "`{value}` is not a valid boolean value.",
            value=value
        )

    @staticmethod
    def get_choices():
        return {
            TranslationsManager().get(Locale.en_US).gettext("True"): "True",
            TranslationsManager().get(Locale.en_US).gettext("False"): "False"
        }

    @staticmethod
    def get_choice_localizations():
        return {
            TranslationsManager().get(Locale.en_US).gettext("True"): {
                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("True"),
                Locale.fr: TranslationsManager().get(Locale.fr).gettext("True"),
            },
            TranslationsManager().get(Locale.en_US).gettext("False"): {
                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("False"),
                Locale.fr: TranslationsManager().get(Locale.fr).gettext("False"),
            }
        }
