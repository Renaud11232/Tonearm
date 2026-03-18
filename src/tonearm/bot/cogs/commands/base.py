from discord.ext import commands
from injector import Injector


class CogBase(commands.Cog):

    def __init__(self, injector: Injector) -> None:
        super().__init__()
        self.__injector = injector

    @property
    def injector(self) -> Injector:
        return self.__injector
