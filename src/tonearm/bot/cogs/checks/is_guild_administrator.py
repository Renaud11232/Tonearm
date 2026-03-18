from .any_of import any_of
from .has_guild_permissions import has_guild_permissions
from .is_guild_owner import is_guild_owner


def is_guild_administrator():
    return any_of(
        has_guild_permissions(administrator=True),
        is_guild_owner()
    )
