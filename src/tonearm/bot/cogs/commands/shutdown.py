import nextcord
from nextcord.ext import commands, application_checks

class ShutdownCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.__bot = bot

    @nextcord.slash_command(
        description="Shuts the bot down"
    )
    @application_checks.is_owner()
    async def shutdown(self, interaction: nextcord.Interaction):
        await interaction.send(":sleeping: Time for a quick nap...")
        await self.__bot.close()