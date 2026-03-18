from tonearm.bot.exceptions import TonearmConverterException


class DurationTransformerException(TonearmConverterException):
    pass

class LoopModeTransformerException(TonearmConverterException):
    pass

class BooleanTransformerException(TonearmConverterException):
    pass

class LocaleTransformerException(TonearmConverterException):
    pass