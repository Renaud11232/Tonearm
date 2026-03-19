import logging

import discord
from injector import inject, singleton
from discord.ext import commands
from discord import app_commands

from tonearm.bot.managers import EmbedManager, StorageManager
from tonearm.utils import Translatable


@singleton
class AppCommandErrorListener(commands.Cog):

    @inject
    def __init__(self,
                 embed_manager: EmbedManager,
                 storage_manager: StorageManager):
        super().__init__()
        self.__embed_manager = embed_manager
        self.__storage_manager = storage_manager
        self.__logger = logging.getLogger("tonearm.listeners")

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        self.__logger.debug(f"Failed to handle command (interaction:{interaction.id}) due to exception : {repr(error)}")
        if isinstance(error, app_commands.CheckFailure):
            await self.__on_check_failure(interaction, error)
        elif isinstance(error, app_commands.TransformerError):
            await self.__on_transformer_error(interaction, error)
        elif isinstance(error, app_commands.CommandInvokeError):
            await self.__on_command_invoke_error(interaction, error.original)
        else:
            self.__logger.error(f"Ignoring AppCommandError in interaction {repr(interaction)}", exc_info=error)

    async def __on_check_failure(self, interaction: discord.Interaction, error: app_commands.CheckFailure):
        if isinstance(error, Translatable):
            await self.__send_ephemeral_error(interaction, error)
        else:
            await self.__send_ephemeral_error(interaction, Translatable("You don't have the permission to use this command."))

    async def __on_transformer_error(self, interaction: discord.Interaction, error: app_commands.TransformerError):
        if isinstance(error, Translatable):
            await self.__send_ephemeral_error(interaction, error)
        else:
            self.__logger.error(f"Ignoring TransformerError in interaction {repr(interaction)}", exc_info=error)

    async def __on_command_invoke_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, Translatable):
            await self.__send_followup_error(interaction, error)
        else:
            self.__logger.error(f"Ignoring CommandInvokeError in interaction {repr(interaction)} caused by", exc_info=error)

    async def __send_ephemeral_error(self, interaction: discord.Interaction, error: Translatable):
        await interaction.response.send_message(
            embed=self.__embed_manager.get(interaction.guild).error(error),
            ephemeral=True
        )

    async def __send_followup_error(self, interaction: discord.Interaction, error: Translatable):
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).error(error),
        )