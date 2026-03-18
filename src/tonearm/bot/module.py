from tonearm.bot import TonearmBot

from discord.ext import commands

from injector import Module, Binder


class BotModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(commands.Bot, to=TonearmBot)
