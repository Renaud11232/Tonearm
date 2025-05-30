import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import PlayerManager
from tonearm.exceptions import TonearmException

class StopCommand(commands.Cog):

    def __init__(self, player_manager: PlayerManager):
        super().__init__()
        self.__player_manager = player_manager

    @nextcord.slash_command(
        description="Stops the current playback"
    )
    async def stop(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        player = self.__player_manager.get_player(interaction.guild)
        try:
            await player.stop(interaction.user.voice)
            await interaction.followup.send(f":vertical_traffic_light: Stopped playback")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")