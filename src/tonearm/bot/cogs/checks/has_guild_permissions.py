import discord
from discord import app_commands

#TODO: reimplement or delete
class HasGuildPermissions:

    def __call__(self, **perms):
        invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
        if invalid:
            raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")
        def predicate(interaction: discord.Interaction) -> bool:
            ch = interaction.channel
            try:
                permissions = ch.permissions_for(interaction.user)
            except AttributeError:
                raise app_commands.NoPrivateMessage()

            missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
            if not missing:
                return True
            raise app_commands.MissingPermissions(missing)
        return app_commands.check(predicate)