import nextcord
from nextcord.ext import commands
import logging

from tonearm.bot.managers import ServiceManager
from tonearm.bot.exceptions import TonearmException

class PlayCommand(commands.Cog):

    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Play a track or playlist in your voice channel. You can provide link, or search for a track"
    )
    async def play(self, interaction: nextcord.Interaction, query: str):
        self.__logger.debug(f"Handling play command (interaction:{interaction.id})")
        await interaction.response.defer()
        player = self.__service_manager.get_player(interaction.guild)
        try:
            tracks = await player.play(interaction.user, query)
            if len(tracks) == 1:
                await interaction.followup.send(f":cd: Added **{tracks[0].title}** to the queue.")
            else:
                await interaction.followup.send(f":cd: Added **{len(tracks)} tracks** to the queue.")
            self.__logger.debug(f"Successfully handled play command (interaction:{interaction.id}), adding {len(tracks)} tracks to the queue")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")
            self.__logger.debug(f"Failed to handle play command (interaction:{interaction.id}) due to exception : {repr(e)}")