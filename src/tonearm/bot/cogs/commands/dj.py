import logging

import nextcord
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import SettingsManager
from tonearm.bot.services import EmbedService


@singleton
class DjCommand(commands.Cog):

    @inject
    def __init__(self, settings_manager: SettingsManager, embed_service: EmbedService):
        super().__init__()
        self.__settings_manager = settings_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

    @nextcord.slash_command(
        description="Manages the DJ roles and members"
    )
    async def dj(self, interaction: nextcord.Interaction):
        pass

    @dj.subcommand(
        description="Adds a role or member to the DJs"
    )
    async def add(self, interaction: nextcord.Interaction):
        pass

    @add.subcommand(
        description="Adds a role to the DJs",
        name="role"
    )
    async def add_role(self, interaction: nextcord.Interaction, role: nextcord.Role):
        self.__logger.debug(f"Handling dj add role command (interaction:{interaction.id})")
        await interaction.response.defer()
        settings_service = await self.__settings_manager.get(interaction.guild)
        await settings_service.add_dj_role(role)
        await interaction.followup.send(
            embed=self.__embed_service.dj_add_role(role)
        )
        self.__logger.debug(f"Successfully handled dj add role command (interaction:{interaction.id})")

    @add.subcommand(
        description="Adds a member to the DJs",
        name="member"
    )
    async def add_member(self, interaction: nextcord.Interaction, member: nextcord.Member):
        self.__logger.debug(f"Handling dj add member command (interaction:{interaction.id})")
        await interaction.response.defer()
        settings_service = await self.__settings_manager.get(interaction.guild)
        await settings_service.add_dj(member)
        await interaction.followup.send(
            embed=self.__embed_service.dj_add_member(member)
        )
        self.__logger.debug(f"Successfully handled dj add member command (interaction:{interaction.id})")

    @dj.subcommand(
        description="Removes a role or member from the DJs"
    )
    async def remove(self, interaction: nextcord.Interaction):
        pass

    @remove.subcommand(
        description="Removes a role from the DJs",
        name="role"
    )
    async def remove_role(self, interaction: nextcord.Interaction, role: nextcord.Role):
        self.__logger.debug(f"Handling dj remove role command (interaction:{interaction.id})")
        await interaction.response.defer()
        settings_service = await self.__settings_manager.get(interaction.guild)
        await settings_service.remove_dj_role(role)
        await interaction.followup.send(
            embed=self.__embed_service.dj_remove_role(role)
        )
        self.__logger.debug(f"Successfully handled dj remove role command (interaction:{interaction.id})")

    @remove.subcommand(
        description="Removes a member from the DJs",
        name="member"
    )
    async def remove_member(self, interaction: nextcord.Interaction, member: nextcord.Member):
        self.__logger.debug(f"Handling dj remove member command (interaction:{interaction.id})")
        await interaction.response.defer()
        settings_service = await self.__settings_manager.get(interaction.guild)
        await settings_service.remove_dj(member)
        await interaction.followup.send(
            embed=self.__embed_service.dj_remove_member(member)
        )
        self.__logger.debug(f"Successfully handled dj remove member command (interaction:{interaction.id})")