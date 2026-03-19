from typing import Any

from discord import AppCommandOptionType
from discord.app_commands import TransformerError, Transformer

from tonearm.utils import Translatable

class TranslatableTransformerError(TransformerError, Translatable):
    def __init__(self, value: Any, opt_type: AppCommandOptionType, transformer: Transformer, msgid: str, /, **kwargs):
        TransformerError.__init__(self, value, opt_type, transformer)
        Translatable.__init__(self, msgid, **kwargs)