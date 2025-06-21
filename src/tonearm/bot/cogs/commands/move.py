import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class MoveCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Moves the position of a track in the queue"
    )
    async def move(self,
                   interaction: nextcord.Interaction,
                   fr0m: int = SlashOption(name="from", required=True, min_value=1),
                   to: int = SlashOption(required=True, min_value=1)):
        self.__logger.debug(f"Handling `move` command (interaction:{interaction.id})")
        await interaction.response.defer()
        player_service = await self.__player_manager.get(interaction.guild)
        moved_track = await player_service.move(interaction.user, fr0m, to)
        await interaction.followup.send(
            embed=self.__embed_service.move(moved_track, fr0m, to)
        )
        self.__logger.debug(f"Successfully handled `move` command (interaction:{interaction.id})")