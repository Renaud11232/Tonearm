import logging

import nextcord
from injector import inject, singleton
from nextcord.ext import commands
from nextcord.errors import ApplicationCheckFailure
from nextcord.ext.application_checks import ApplicationNoPrivateMessage

from tonearm.bot.cogs.checks.exceptions import IsAnarchy, NotCorrectChannel
from tonearm.bot.exceptions import TonearmCommandException
from tonearm.bot.managers import EmbedManager, StorageManager


@singleton
class ApplicationCommandErrorListener(commands.Cog):

    @inject
    def __init__(self,
                 embed_manager: EmbedManager,
                 storage_manager: StorageManager):
        super().__init__()
        self.__embed_manager = embed_manager
        self.__storage_manager = storage_manager
        self.__logger = logging.getLogger("tonearm.listeners")

    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        self.__logger.debug(f"Failed to handle command (interaction:{interaction.id}) due to exception : {repr(error)}")
        if isinstance(error, ApplicationCheckFailure):
            if isinstance(error, ApplicationNoPrivateMessage):
                return
            elif isinstance(error, IsAnarchy):
                embed = self.__embed_manager.get(interaction.guild).error_message("Anarchy rules here, votes are disabled !")
            elif isinstance(error, NotCorrectChannel):
                embed = self.__embed_manager.get(interaction.guild).error_message(
                    "I'm only accepting commands in the {channel} channel.",
                    channel=self.__storage_manager.get(interaction.guild).get_channel().mention
                )
            else:
                embed = self.__embed_manager.get(interaction.guild).error_message("You don't have the permission to use this command.")
            await interaction.send(
                ephemeral=True,
                embed=embed
            )
        elif isinstance(error, nextcord.ApplicationInvokeError):
            exception = error.original
            if isinstance(exception, TonearmCommandException):
                await interaction.followup.send(
                    embed=self.__embed_manager.get(interaction.guild).error(exception)
                )
            else:
                raise error
        else:
            raise error