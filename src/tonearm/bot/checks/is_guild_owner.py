import nextcord
from nextcord.ext import application_checks


class IsGuildOwner:

    def __call__(self):
        def predicate(interaction: nextcord.Interaction) -> bool:
            return interaction.guild.owner_id == interaction.user.id
        return application_checks.check(predicate)