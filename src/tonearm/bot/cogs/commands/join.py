import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import PlayerManager
from tonearm.exceptions import TonearmException


class JoinCommand(commands.Cog):

    def __init__(self, queue_manager: PlayerManager):
        self.__queue_manager = queue_manager

    @nextcord.slash_command(
        description="Joins your current voice channel"
    )
    async def join(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        player = self.__queue_manager.get_player(interaction.guild)
        try:
            await player.join(interaction.user.voice)
            await interaction.followup.send(f":microphone: Ready to rock and roll !")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")