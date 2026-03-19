from typing import Any

from discord import AppCommandOptionType
from discord.app_commands import CheckFailure, TransformerError, AppCommandError, Transformer

from tonearm.utils import Translatable


class TranslatableException(Exception, Translatable):
    def __init__(self, msgid: str, /, **kwargs):
        Exception.__init__(self, msgid.format(**kwargs))
        Translatable.__init__(self, msgid, **kwargs)


#FIXME Is this compatible with discord.py, check all exceptions in fact
class TonearmException(AppCommandError):
    def __init__(self, template: str, **kwargs):
        super().__init__(template.format(**kwargs))
        self.__template = template
        self.__kwargs = kwargs

    @property
    def template(self):
        return self.__template

    @property
    def kwargs(self):
        return self.__kwargs

class TonearmCommandException(TonearmException):
    pass
