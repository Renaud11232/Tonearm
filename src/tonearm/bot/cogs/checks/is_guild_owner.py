import discord
from discord import app_commands


def is_guild_owner():
    async def predicate(interaction: discord.Interaction) -> bool:
        return interaction.guild.owner_id  == interaction.user.id
    return app_commands.check(predicate)
