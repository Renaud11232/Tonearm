from gettext import NullTranslations
from typing import Optional

from discord import app_commands, Locale
from discord.app_commands import locale_str, TranslationContextTypes

from tonearm.bot.managers.translations import TranslationsManager


class TonearmTranslator(app_commands.Translator):
    async def translate(self, string: locale_str, locale: Locale, context: TranslationContextTypes) -> Optional[str]:
        translations = TranslationsManager().get(locale)
        if isinstance(translations, NullTranslations):
            return None
        return translations.gettext(str(string))