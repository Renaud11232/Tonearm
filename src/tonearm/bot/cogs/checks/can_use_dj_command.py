from .any_of import any_of
from .is_guild_administrator import is_guild_administrator
from .is_anarchy import is_anarchy
from .is_dj_member import is_dj_member
from .has_dj_role import has_dj_role


def can_use_dj_command():
    return any_of(
        is_anarchy(),
        has_dj_role(),
        is_dj_member(),
        is_guild_administrator()
    )
