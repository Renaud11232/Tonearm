class CobaltException(Exception):

    def __init__(self, code: str, context: dict | None = None):
        super().__init__(code)
        self.__code = code
        self.__context = context

    @property
    def code(self):
        return self.__code

    @property
    def context(self):
        return self.__context