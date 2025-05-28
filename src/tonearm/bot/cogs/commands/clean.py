import nextcord
from nextcord.ext import commands

class Clean(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super(Clean, self).__init__()
        self.__bot = bot

    @nextcord.slash_command(
        description="Deletes all bot messages in the channel"
    )
    async def clean(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        messages = 0
        async for message in interaction.channel.history():
            if message.author == self.__bot.user:
                messages += 1
                await message.delete()
        await interaction.followup.send(f":wastebasket: All messages cleaned ({messages})")