from discord.app_commands import AppCommandError

#FIXME Is this compatible with discord.py, check all exceptions in fact
class TonearmException(AppCommandError):
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
