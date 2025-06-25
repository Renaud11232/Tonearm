import logging

import nextcord
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.managers import DjManager
from tonearm.bot.services import EmbedService
from tonearm.bot.cogs.checks import IsGuildAdministrator

from .base import CommandCogBase


@singleton
class DjCommand(CommandCogBase):

    @inject
    def __init__(self, dj_manager: DjManager, embed_service: EmbedService, is_guild_administrator: IsGuildAdministrator):
        super().__init__()
        self.__dj_manager = dj_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.add, self.remove, checks=[
            application_checks.guild_only(),
            is_guild_administrator()
        ])

    @nextcord.slash_command(
        description="Manages the DJ roles and members"
    )
    async def dj(self, interaction: nextcord.Interaction):
        pass

    @dj.subcommand(
        description="Adds a role or member to the DJs"
    )
    async def add(self, interaction: nextcord.Interaction, dj: nextcord.Mentionable):
        self.__logger.debug(f"Handling `dj add` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__dj_manager.get(interaction.guild).add(dj) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_service.dj_add(dj) # type: ignore
        )
        self.__logger.debug(f"Successfully handled `dj add` command (interaction:{interaction.id})")

    @dj.subcommand(
        description="Removes a role or member from the DJs"
    )
    async def remove(self, interaction: nextcord.Interaction, dj: nextcord.Mentionable):
        self.__logger.debug(f"Handling `dj remove` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__dj_manager.get(interaction.guild).remove(dj) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_service.dj_remove(dj) # type: ignore
        )
        self.__logger.debug(f"Successfully handled `dj remove` command (interaction:{interaction.id})")
