import gettext
import os
from typing import Union

from discord import Locale

from injector import singleton, inject

from tonearm.bot.managers.base import ManagerBase


@singleton
class TranslationsManager(ManagerBase[Locale, Union[gettext.GNUTranslations, gettext.NullTranslations]]):

    def __init__(self):
        super().__init__()

    def _get_id(self, key: Locale) -> str:
        return key.value

    def _create(self, key: Locale) -> Union[gettext.GNUTranslations, gettext.NullTranslations]:
        return gettext.translation(
            domain="messages",
            localedir=os.path.join(os.path.dirname(__file__), "locales"),
            languages=[self._get_id(key)],
            fallback=True
        )