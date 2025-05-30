import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import PlayerManager
from tonearm.exceptions import TonearmException

class NextCommand(commands.Cog):

    def __init__(self, player_manager: PlayerManager):
        super().__init__()
        self.__player_manager = player_manager

    @nextcord.slash_command(
        description="Skips the current playing track to the next one"
    )
    async def next(self, interaction: nextcord.Interaction):
        await self.__next(interaction)

    @nextcord.slash_command(
        description="Skips the current playing track to the next one"
    )
    async def skip(self, interaction: nextcord.Interaction):
        await self.__next(interaction)

    async def __next(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        player = self.__player_manager.get_player(interaction.guild)
        try:
            await player.next(interaction.user)
            await interaction.followup.send(f":fast_forward: Skipping to the next track, I didn't like this one either")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")