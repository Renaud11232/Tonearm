import nextcord
from nextcord.ext import commands

class NowCommand(commands.Cog):

    @nextcord.slash_command(
        description="Shows the current playing track"
    )
    async def now(self, interaction: nextcord.Interaction):
        await self.__now(interaction)

    @nextcord.slash_command(
        name="now-playing",
        description="Shows the current playing track"
    )
    async def now_playing(self, interaction: nextcord.Interaction):
        await self.__now(interaction)

    @staticmethod
    async def __now(interaction: nextcord.Interaction):
        #TODO :musical_note: Now playing : {track_title} by {artist}. Enjoy !
        await interaction.send(":wrench: This feature is not implemented yet !")