import gettext
import os
from typing import Union

from nextcord import Locale

from tonearm.bot.managers.base import ManagerBase
from tonearm.utils.singleton import ABCMetaSingleton


class TranslationsManager(ManagerBase[Locale, Union[gettext.GNUTranslations, gettext.NullTranslations]], metaclass=ABCMetaSingleton):

    def __init__(self):
        super().__init__()

    def _get_id(self, key: Locale) -> str:
        return str(key)

    def _create(self, key: Locale) -> Union[gettext.GNUTranslations, gettext.NullTranslations]:
        return gettext.translation(
            domain="messages",
            localedir=os.path.join(os.path.dirname(__file__), "locales"),
            languages=[self._get_id(key)],
            fallback=True
        )