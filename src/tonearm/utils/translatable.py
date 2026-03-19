class Translatable:
    def __init__(self, msgid: str, /, **kwargs):
        self.__msgid = msgid
        self.__kwargs = kwargs

    @property
    def msgid(self):
        return self.__msgid

    @property
    def kwargs(self):
        return self.__kwargs