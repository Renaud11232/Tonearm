import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import PlayerManager
from tonearm.exceptions import TonearmException


class JoinCommand(commands.Cog):

    def __init__(self, player_manager: PlayerManager):
        super().__init__()
        self.__player_manager = player_manager

    @nextcord.slash_command(
        description="Joins your current voice channel"
    )
    async def join(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        player = self.__player_manager.get_player(interaction.guild)
        try:
            await player.join(interaction.user.voice)
            await interaction.followup.send(f":microphone: Ready to rock and roll !")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")