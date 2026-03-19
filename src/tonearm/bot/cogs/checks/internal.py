from typing import Callable

import discord
from discord import app_commands
from discord.app_commands.commands import Check, T

from tonearm.bot.cogs.base import InjectorCog


def dependency_needing_check(predicate: Check):
    async def p(interaction: discord.Interaction) -> bool:
        cog = interaction.command.binding
        if isinstance(cog, InjectorCog):
            return await discord.utils.maybe_coroutine(cog.injector.call_with_injection, predicate, args=(interaction,))
        return await discord.utils.maybe_coroutine(predicate, interaction)
    return app_commands.check(p)

def recover_predicates(*check_decorators: Callable[[T], T]) -> list[Check]:
    def func():
        pass
    for check_decorator in check_decorators:
        check_decorator(func)
    return func.__discord_app_commands_checks__