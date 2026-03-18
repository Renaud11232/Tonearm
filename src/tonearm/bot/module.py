from tonearm.bot import TonearmBot

from discord.ext import commands

from injector import Module, singleton, provider


class BotModule(Module):

    #TODO: check if this is really needed ?
    @singleton
    @provider
    def provide_bot(self, tonearm_bot: TonearmBot) -> commands.Bot:
        return tonearm_bot
