from nextcord.errors import ApplicationError


class TonearmException(ApplicationError):
    def __init__(self, template: str, **kwargs):
        super().__init__(template.format(**kwargs))
        self.__template = template
        self.__kwargs = kwargs

    @property
    def template(self):
        return self.__template

    @property
    def kwargs(self):
        return self.__kwargs

class TonearmConverterException(TonearmException):
    pass

class TonearmCommandException(TonearmException):
    pass
