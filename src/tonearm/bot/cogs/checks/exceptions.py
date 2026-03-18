from discord.app_commands.errors import CheckFailure


class IsAnarchy(CheckFailure):
    pass

class NotCorrectChannel(CheckFailure):
    pass
