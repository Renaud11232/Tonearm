from nextcord.errors import ApplicationCheckFailure


class TonearmCheckException(ApplicationCheckFailure):
    pass

class TonearmConverterException(Exception):
    pass

class TonearmCommandException(Exception):
    pass
