import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.cogs.checks import is_correct_channel, is_not_anarchy
from tonearm.bot.managers import EmbedManager, PlayerManager
from tonearm.bot.cogs.base import InjectorCog


@singleton
class VotenextCommand(InjectorCog):

    @inject
    def __init__(self,
                 player_manager: PlayerManager,
                 embed_manager: EmbedManager,
                 injector: Injector):
        super().__init__(injector)
        self.__player_manager = player_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @app_commands.command(
        name="votenext",
        description=app_commands.locale_str("Vote to skip the current track"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @is_not_anarchy()
    async def votenext(self, interaction: discord.Interaction):
        await self.__votenext(interaction)

    @app_commands.command(
        name="voteskip",
        description=app_commands.locale_str("Vote to skip the current track"),
        auto_locale_strings=False
    )
    @app_commands.guild_only()
    @is_correct_channel()
    @is_not_anarchy()
    async def voteskip(self, interaction: discord.Interaction):
        await self.__votenext(interaction)

    async def __votenext(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `votenext` command (interaction:{interaction.id})")
        await interaction.response.defer()
        status = await self.__player_manager.get(interaction.guild).votenext(interaction.user)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).votenext(status)
        )
        self.__logger.debug(f"Successfully handled `votenext` command (interaction:{interaction.id})")
