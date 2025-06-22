class TonearmException(Exception):
    pass

class TonearmCheckException(TonearmException):
    pass

class TonearmConverterException(TonearmException):
    pass

class TonearmInvokeException(TonearmException):
    pass
#TODO: Check if best to use nextcord Exception super classes