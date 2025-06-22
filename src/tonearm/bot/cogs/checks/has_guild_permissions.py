import nextcord
from nextcord.ext import application_checks


class HasGuildPermissions:

    def __call__(self, **perms):
        invalid = set(perms) - set(nextcord.Permissions.VALID_FLAGS)
        if invalid:
            raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")
        def predicate(interaction: nextcord.Interaction) -> bool:
            ch = interaction.channel
            try:
                permissions = ch.permissions_for(interaction.user)
            except AttributeError:
                raise application_checks.ApplicationNoPrivateMessage()

            missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
            if not missing:
                return True
            raise application_checks.ApplicationMissingPermissions(missing)
        return application_checks.check(predicate)