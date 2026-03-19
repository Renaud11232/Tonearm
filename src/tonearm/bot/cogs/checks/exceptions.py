from discord.app_commands import CheckFailure

from tonearm.utils import Translatable


class TranslatableCheckFailure(CheckFailure, Translatable):
    def __init__(self, msgid: str, /, **kwargs):
        CheckFailure.__init__(self)
        Translatable.__init__(self, msgid, **kwargs)