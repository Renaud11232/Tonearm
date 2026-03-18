from gettext import GNUTranslations
from typing import Optional

from discord import app_commands, Locale
from discord.app_commands import locale_str, TranslationContextTypes

from injector import singleton, inject

from tonearm.bot.managers.translations import TranslationsManager


@singleton
class TonearmTranslator(app_commands.Translator):

    @inject
    def __init__(self, translations_manager: TranslationsManager):
        super().__init__()
        self.__translations_manager = translations_manager

    async def translate(self, string: locale_str, locale: Locale, context: TranslationContextTypes) -> Optional[str]:
        translations = self.__translations_manager.get(locale)
        if not isinstance(translations, GNUTranslations):
            return None
        return translations.gettext(str(string))