from discord import app_commands


class DurationTransformerException(app_commands.TransformerError):
    pass

class LoopModeTransformerException(app_commands.TransformerError):
    pass

class BooleanTransformerException(app_commands.TransformerError):
    pass

class LocaleTransformerException(app_commands.TransformerError):
    pass