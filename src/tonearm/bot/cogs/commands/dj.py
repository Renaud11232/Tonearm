import logging

import nextcord
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import DjManager
from tonearm.bot.services import EmbedService


@singleton
class DjCommand(commands.Cog):

    @inject
    def __init__(self, dj_manager: DjManager, embed_service: EmbedService):
        super().__init__()
        self.__dj_manager = dj_manager
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
        dj_service = await self.__dj_manager.get(interaction.guild)
        await dj_service.add_role(role)
        await interaction.followup.send(
            embed=self.__embed_service.dj_add(role)
        )
        self.__logger.debug(f"Successfully handled dj add role command (interaction:{interaction.id})")

    @add.subcommand(
        description="Adds a member to the DJs",
        name="member"
    )
    async def add_member(self, interaction: nextcord.Interaction, member: nextcord.Member):
        self.__logger.debug(f"Handling dj add member command (interaction:{interaction.id})")
        await interaction.response.defer()
        dj_service = await self.__dj_manager.get(interaction.guild)
        await dj_service.add(member)
        await interaction.followup.send(
            embed=self.__embed_service.dj_add(member)
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
        dj_service = await self.__dj_manager.get(interaction.guild)
        await dj_service.remove_role(role)
        await interaction.followup.send(
            embed=self.__embed_service.dj_remove(role)
        )
        self.__logger.debug(f"Successfully handled dj remove role command (interaction:{interaction.id})")

    @remove.subcommand(
        description="Removes a member from the DJs",
        name="member"
    )
    async def remove_member(self, interaction: nextcord.Interaction, member: nextcord.Member):
        self.__logger.debug(f"Handling dj remove member command (interaction:{interaction.id})")
        await interaction.response.defer()
        dj_service = await self.__dj_manager.get(interaction.guild)
        await dj_service.remove(member)
        await interaction.followup.send(
            embed=self.__embed_service.dj_remove(member)
        )
        self.__logger.debug(f"Successfully handled dj remove member command (interaction:{interaction.id})")