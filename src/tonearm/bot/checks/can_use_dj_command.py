from injector import inject

from nextcord.ext import application_checks

from .is_guild_administrator import IsGuildAdministrator
from .is_anarchy import IsAnarchy
from .is_dj_member import IsDjMember
from .has_dj_role import HasDjRole


class CanUseDjCommand:

    @inject
    def __init__(self,
                 is_anarchy: IsAnarchy,
                 has_dj_role: HasDjRole,
                 is_dj_member: IsDjMember,
                 is_guild_administrator: IsGuildAdministrator):
        self.__is_anarchy = is_anarchy
        self.__has_dj_role = has_dj_role
        self.__is_dj_member = is_dj_member
        self.__is_guild_administrator = is_guild_administrator

    def __call__(self):
        return application_checks.check_any(
            self.__is_anarchy(),
            self.__is_dj_member(),
            self.__has_dj_role(),
            self.__is_guild_administrator()
        )
