import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import IsCorrectChannel
from tonearm.bot.cogs.converters import ZeroIndexConverter
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class QueueCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_service: EmbedService,
                 is_correct_channel: IsCorrectChannel):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.queue, checks=[
            application_checks.guild_only(),
            is_correct_channel()
        ])

    @nextcord.slash_command(
        name="queue",
        description="show the current queue"
    )
    async def queue(self,
                    interaction: nextcord.Interaction,
                    page: ZeroIndexConverter = SlashOption(
                        name="page",
                        description="Page to show",
                        required=False,
                        default=0,
                        min_value=1
                    )):
        self.__logger.debug(f"Handling `queue` command (interaction:{interaction.id})")
        await interaction.response.defer()
        status = self.__player_manager.get(interaction.guild).queue(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_service.queue(status, page) # type: ignore
        )
        self.__logger.debug(f"Successfully handled `queue` command (interaction:{interaction.id}, with status : {repr(status)}")