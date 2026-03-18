import logging

import discord
from discord import app_commands

from injector import inject, singleton, Injector

from tonearm.bot.managers import ChatManager, EmbedManager
from tonearm.bot.cogs.checks import is_guild_administrator

from .base import CogBase


@singleton
class CleanCommand(CogBase):

    @inject
    def __init__(self,
                 chat_manager: ChatManager,
                 embed_manager: EmbedManager,
                 injector: Injector):
        super().__init__(injector)
        self.__chat_manager = chat_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @app_commands.command(
        name="clean",
        description=app_commands.locale_str("Delete bot messages in the channel (up to 100 at once)"),
        auto_locale_strings=False
    )
    @app_commands.describe(
        limit=app_commands.locale_str("Maximum number of messages to delete in one run")
    )
    @app_commands.rename(
        limit=app_commands.locale_str("limit")
    )
    @app_commands.guild_only()
    @is_guild_administrator()
    async def clean(self,
                    interaction: discord.Interaction,
                    limit: app_commands.Range[int, 1, 100]):
        self.__logger.debug(f"Handling `clean` command (interaction:{interaction.id})")
        await interaction.response.defer(ephemeral=True)
        messages = await self.__chat_manager.get(interaction.channel).clean(limit)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).clean(messages)
        )
        self.__logger.debug(f"Successfully handled `clean` command (interaction:{interaction.id}), deleting {len(messages)} messages")
