import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.managers import ChatManager
from tonearm.bot.services import EmbedService
from tonearm.bot.cogs.checks import IsGuildAdministrator

from .base import CommandCogBase


@singleton
class CleanCommand(CommandCogBase):

    @inject
    def __init__(self,
                 chat_manager: ChatManager,
                 embed_service: EmbedService,
                 is_guild_administrator: IsGuildAdministrator):
        super().__init__()
        self.__chat_manager = chat_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.clean, checks=[
            application_checks.guild_only(),
            is_guild_administrator()
        ])

    @nextcord.slash_command(
        description="Deletes bot messages in the channel (up to 100 at once)"
    )
    async def clean(self,
                    interaction: nextcord.Interaction,
                    limit: int = SlashOption(required=True, min_value=1, max_value=100)):
        self.__logger.debug(f"Handling `clean` command (interaction:{interaction.id})")
        await interaction.response.defer(ephemeral=True)
        messages = await self.__chat_manager.get(interaction.channel).clean(limit)
        await interaction.followup.send(
            embed=self.__embed_service.clean(messages)
        )
        self.__logger.debug(f"Successfully handled `clean` command (interaction:{interaction.id}), deleting {len(messages)} messages")