import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.managers import DjManager, EmbedManager
from tonearm.bot.cogs.checks import is_guild_administrator

from .base import CogBase


@singleton
class DjCommand(CogBase):

    dj = app_commands.Group(
        name="dj",
        description="Manage DJ roles and members", #TODO: add translation
        allowed_contexts=app_commands.AppCommandContext(
            guild=True,
            dm_channel=False,
            private_channel=False
        )
    )

    @inject
    def __init__(self,
                 dj_manager: DjManager,
                 embed_manager: EmbedManager,
                 injector: Injector):
        super().__init__(injector)
        self.__dj_manager = dj_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @dj.command(
        name="add",
        description="Add a role or member to the DJs"
    )
    @app_commands.describe(
        dj="Role or member to add to the DJs"
    )
    @is_guild_administrator()
    async def dj_add(self,
                     interaction: discord.Interaction,
                     dj: discord.Member | discord.Role):
        self.__logger.debug(f"Handling `dj add` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__dj_manager.get(interaction.guild).add(dj)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).dj_add(dj)
        )
        self.__logger.debug(f"Successfully handled `dj add` command (interaction:{interaction.id})")

    @dj.command(
        name="remove",
        description="Remove a role or member from the DJs"
    )
    @app_commands.describe(
        dj="Role or member to remove from the DJs"
    )
    @is_guild_administrator()
    async def dj_remove(self,
                        interaction: discord.Interaction,
                        dj: discord.Member | discord.Role):
        self.__logger.debug(f"Handling `dj remove` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__dj_manager.get(interaction.guild).remove(dj)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).dj_remove(dj)
        )
        self.__logger.debug(f"Successfully handled `dj remove` command (interaction:{interaction.id})")
