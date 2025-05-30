import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import PlayerManager
from tonearm.exceptions import TonearmException

class LeaveCommand(commands.Cog):

    def __init__(self, bot: commands.Bot, player_manager: PlayerManager):
        super().__init__()
        self.__bot = bot
        self.__player_manager = player_manager

    @nextcord.slash_command(
        description="Leaves the current voice channel"
    )
    async def leave(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        player = self.__player_manager.get_player(interaction.guild)
        try:
            await player.leave(interaction.user)
            await interaction.followup.send(f":wave: Goodbye !")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")
