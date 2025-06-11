import logging

import nextcord
from nextcord.ext import commands

from injector import inject

from tonearm.bot.managers import ServiceManager


class PlayCommand(commands.Cog):

    @inject
    def __init__(self, service_manager: ServiceManager):
        super().__init__()
        self.__service_manager = service_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Play a track or playlist in your voice channel. You can provide link, or search for a track"
    )
    async def play(self, interaction: nextcord.Interaction, query: str):
        await interaction.response.defer()
        self.__logger.debug(f"Handling play command (interaction:{interaction.id})")
        tracks = await self.__service_manager.get_player(interaction.guild).play(interaction.user, query)
        if len(tracks) == 1:
            await interaction.followup.send(f":cd: **{tracks[0].title}** added ! This one’s gonna slap.")
        else:
            await interaction.followup.send(f":cd: Added {len(tracks)} tracks to the queue! Now that’s what I call a playlist.")
        self.__logger.debug(f"Successfully handled play command (interaction:{interaction.id}), adding {len(tracks)} tracks to the queue")