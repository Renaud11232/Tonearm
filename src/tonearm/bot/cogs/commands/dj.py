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
        description=app_commands.locale_str("Manage DJ roles and members"),
        guild_only=True,
        auto_locale_strings=False
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
        description=app_commands.locale_str("Add a role or member to the DJs"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        dj=app_commands.locale_str("Role or member to add to the DJs")
    )
    @app_commands.rename(
        dj=app_commands.locale_str("dj")
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
        description=app_commands.locale_str("Remove a role or member from the DJs"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        dj=app_commands.locale_str("Role or member to remove from the DJs")
    )
    @app_commands.rename(
        dj=app_commands.locale_str("dj")
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
