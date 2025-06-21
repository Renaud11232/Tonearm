class TonearmException(Exception):
    pass

class TonearmCheckException(TonearmException):
    pass

class TonearmConverterException(TonearmException):
    pass

class TonearmInvokeException(TonearmException):
    pass