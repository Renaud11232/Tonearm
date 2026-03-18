from discord import app_commands

from .any_of import any_of
from .is_guild_owner import is_guild_owner


def is_guild_administrator():
    return any_of(
        app_commands.checks.has_permissions(administrator=True),
        is_guild_owner()
    )
