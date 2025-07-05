import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import inject, singleton

from tonearm.bot.managers import ChatManager, TranslationsManager, EmbedManager
from tonearm.bot.cogs.checks import IsGuildAdministrator

from .base import CommandCogBase


@singleton
class CleanCommand(CommandCogBase):

    @inject
    def __init__(self,
                 chat_manager: ChatManager,
                 embed_manager: EmbedManager,
                 is_guild_administrator: IsGuildAdministrator):
        super().__init__()
        self.__chat_manager = chat_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.clean, checks=[
            application_checks.guild_only(),
            is_guild_administrator()
        ])

    @nextcord.slash_command(
        name="clean",
        description=TranslationsManager().get(Locale.en_US).gettext("Delete bot messages in the channel (up to 100 at once)"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Delete bot messages in the channel (up to 100 at once)"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Delete bot messages in the channel (up to 100 at once)")
        }
    )
    async def clean(self,
                    interaction: nextcord.Interaction,
                    limit: int = SlashOption(
                        name=TranslationsManager().get(Locale.en_US).gettext("limit"),
                        name_localizations={
                            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("limit"),
                            Locale.fr: TranslationsManager().get(Locale.fr).gettext("limit")
                        },
                        description=TranslationsManager().get(Locale.en_US).gettext("Maximum number of messages to delete in one run"),
                        description_localizations={
                            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Maximum number of messages to delete in one run"),
                            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Maximum number of messages to delete in one run")
                        },
                        required=True,
                        min_value=1,
                        max_value=100
                    )):
        self.__logger.debug(f"Handling `clean` command (interaction:{interaction.id})")
        await interaction.response.defer(ephemeral=True)
        messages = await self.__chat_manager.get(interaction.channel).clean(limit)  # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).clean(messages)
        )
        self.__logger.debug(f"Successfully handled `clean` command (interaction:{interaction.id}), deleting {len(messages)} messages")
