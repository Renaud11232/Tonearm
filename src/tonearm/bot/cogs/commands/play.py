import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import PlayerManager
from tonearm.exceptions import TonearmException

class PlayCommand(commands.Cog):

    def __init__(self, player_manager: PlayerManager):
        super().__init__()
        self.__player_manager = player_manager

    @nextcord.slash_command(
        description="Play a track or playlist in your voice channel. You can provide link, or search for a track"
    )
    async def play(self, interaction: nextcord.Interaction, query: str):
        await interaction.response.defer()
        player = self.__player_manager.get_player(interaction.guild)
        try:
            tracks = await player.play(interaction.user.voice, query)
            if len(tracks) == 1:
                await interaction.followup.send(f":cd: Added **{tracks[0].title}** to the queue.")
            else:
                await interaction.followup.send(f":cd: Added **{len(tracks)} tracks** to the queue.")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")