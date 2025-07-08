import nextcord

from .exceptions import LocaleConverterException


class LocaleConverter(nextcord.OptionConverter):

    __LOCALE_NAMES = [locale.name for locale in nextcord.Locale]
    __SUPPORTED_LOCALES = [
        nextcord.Locale.en_US,
        nextcord.Locale.fr
    ]

    def __init__(self):
        super().__init__(str)

    async def convert(self, interaction: nextcord.Interaction, value: str) -> nextcord.Locale | None:
        if value is None:
            return None
        if value not in LocaleConverter.__LOCALE_NAMES:
            raise LocaleConverterException(
                "`{value}` is not a valid locale.",
                value=value
            )
        return nextcord.Locale[value]  # type: ignore

    @staticmethod
    def get_choices():
        return [
            locale.name for locale in LocaleConverter.__SUPPORTED_LOCALES
        ]