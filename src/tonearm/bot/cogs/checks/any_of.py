from typing import Callable

import discord
from discord import app_commands
from discord.app_commands.commands import T

from .internal import recover_predicates


def any_of(*check_decorators: Callable[[T], T]) -> Callable[[T], T]:
    async def predicate(interaction: discord.Interaction) -> bool:
        for p in recover_predicates(*check_decorators):
            try:
                if await discord.utils.maybe_coroutine(p, interaction):
                    return True
            except app_commands.CheckFailure:
                continue
        return False
    return app_commands.check(predicate)