import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import CanUseDjCommand, IsCorrectChannel
from tonearm.bot.managers import PlayerManager
from tonearm.bot.services import EmbedService

from .base import CommandCogBase


@singleton
class VolumeCommand(CommandCogBase):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_service: EmbedService,
                 is_correct_channel: IsCorrectChannel,
                 can_use_dj_command: CanUseDjCommand):
        super().__init__()
        self.__player_manager = player_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.volume, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            can_use_dj_command()
        ])


    @nextcord.slash_command(
        name="volume",
        description="Changes the volume of the playing tracks"
    )
    async def volume(self,
                     interaction: nextcord.Interaction,
                     volume: int = SlashOption(
                         name="volume",
                         description="Playback volume (between 0 and 200)",
                         required=True,
                         min_value=0,
                         max_value=200
                     )):
        self.__logger.debug(f"Handling `volume` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__player_manager.get(interaction.guild).volume(interaction.user, volume)
        await interaction.followup.send(
            embed=self.__embed_service.volume(volume)
        )
        self.__logger.debug(f"Successfully handled `volume` command (interaction:{interaction.id}, setting volume to : {repr(volume)}")