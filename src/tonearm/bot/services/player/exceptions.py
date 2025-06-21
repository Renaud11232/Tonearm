from tonearm.bot.exceptions import TonearmInvokeException


class PlayerException(TonearmInvokeException):
    pass

class QueueException(PlayerException):
    pass