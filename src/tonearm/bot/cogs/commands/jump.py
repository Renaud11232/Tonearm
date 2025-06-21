import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService


@singleton
class JumpCommand(commands.Cog):

    @inject
    def __init__(self, player_manager: PlayerManager, embed_service: EmbedService):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Jumps to a specific track in the queue"
    )
    async def jump(self,
                   interaction: nextcord.Interaction,
                   track: int = SlashOption(required=False, min_value=1)):
        await self.__jump(interaction, track)

    @nextcord.slash_command(
        description="Jumps to a specific track in the queue"
    )
    async def skipto(self,
                     interaction: nextcord.Interaction,
                     track: int = SlashOption(required=False, min_value=1)):
        await self.__jump(interaction, track)

    async def __jump(self, interaction: nextcord.Interaction, track: int):
        self.__logger.debug(f"Handling `jump` command (interaction:{interaction.id})")
        await interaction.response.defer()
        await self.__player_manager.get(interaction.guild).jump(interaction.user, track)
        await interaction.followup.send(
            embed=self.__embed_service.jump(track)
        )
        self.__logger.debug(f"Successfully handled `jump` command (interaction:{interaction.id})")