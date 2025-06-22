from injector import inject

from nextcord.ext import application_checks

from .has_guild_permissions import HasGuildPermissions
from .is_guild_owner import IsGuildOwner


class IsGuildAdministrator:

    @inject
    def __init__(self, has_guild_permissions: HasGuildPermissions, is_guild_owner: IsGuildOwner):
        self.__has_guild_permissions = has_guild_permissions
        self.__is_guild_owner = is_guild_owner

    def __call__(self):
        return application_checks.check_any(
            self.__has_guild_permissions(administrator=True),
            self.__is_guild_owner(),
        )