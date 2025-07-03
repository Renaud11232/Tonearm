import gettext
import os
from typing import Union

from injector import singleton, inject

from tonearm.bot.managers.base import ManagerBase


@singleton
class I18nManager(ManagerBase[str, Union[gettext.GNUTranslations, gettext.NullTranslations]]):

    @inject
    def __init__(self):
        super().__init__()

    def _get_id(self, key: str) -> str:
        return key

    def _create(self, key: str) -> Union[gettext.GNUTranslations, gettext.NullTranslations]:
        return gettext.translation(
            domain="messages",
            localedir=os.path.join(os.path.dirname(__file__), "locales"),
            languages=[key],
            fallback=True
        )