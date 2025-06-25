from tonearm.bot.exceptions import TonearmCommandException


class PlayerException(TonearmCommandException):
    pass

class QueueException(PlayerException):
    pass