import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.managers import DjManager, TranslationsManager, EmbedManager
from tonearm.bot.cogs.checks import IsGuildAdministrator

from .base import CommandCogBase


@singleton
class DjCommand(CommandCogBase):

    @inject
    def __init__(self,
                 dj_manager: DjManager,
                 embed_manager: EmbedManager,
                 is_guild_administrator: IsGuildAdministrator):
        super().__init__()
        self.__dj_manager = dj_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(self.dj_add, self.dj_remove, checks=[
            application_checks.guild_only(),
            is_guild_administrator()
        ])

    @nextcord.slash_command(
        name="dj"
    )
    async def dj(self, interaction: nextcord.Interaction):
        pass

    @dj.subcommand(
        name="add",
        description=TranslationsManager().get(Locale.en_US).gettext("Add a role or member to the DJs"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Add a role or member to the DJs"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Add a role or member to the DJs")
        }
    )
    async def dj_add(self,
                     interaction: nextcord.Interaction,
                     dj: nextcord.Mentionable = SlashOption(
                         name=TranslationsManager().get(Locale.en_US).gettext("dj"),
                         name_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("dj"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("dj")
                         },
                         description=TranslationsManager().get(Locale.en_US).gettext("Role or member to add to the DJs"),
                         description_localizations={
                             Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Role or member to add to the DJs"),
                             Locale.fr: TranslationsManager().get(Locale.fr).gettext("Role or member to add to the DJs")
                         },
                         required=True
                     )):
        self.__logger.debug(f"Handling `dj add` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__dj_manager.get(interaction.guild).add(dj) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).dj_add(dj) # type: ignore
        )
        self.__logger.debug(f"Successfully handled `dj add` command (interaction:{interaction.id})")

    @dj.subcommand(
        name="remove",
        description=TranslationsManager().get(Locale.en_US).gettext("Remove a role or member from the DJs"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Remove a role or member from the DJs"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Remove a role or member from the DJs")
        }
    )
    async def dj_remove(self,
                        interaction: nextcord.Interaction,
                        dj: nextcord.Mentionable = SlashOption(
                            name=TranslationsManager().get(Locale.en_US).gettext("dj"),
                            name_localizations={
                                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("dj"),
                                Locale.fr: TranslationsManager().get(Locale.fr).gettext("dj")
                            },
                            description=TranslationsManager().get(Locale.en_US).gettext("Role or member to remove from the DJs"),
                            description_localizations={
                                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Role or member to remove from the DJs"),
                                Locale.fr: TranslationsManager().get(Locale.fr).gettext("Role or member to remove from the DJs")
                            },
                            required=True
                        )):
        self.__logger.debug(f"Handling `dj remove` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__dj_manager.get(interaction.guild).remove(dj) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).dj_remove(dj) # type: ignore
        )
        self.__logger.debug(f"Successfully handled `dj remove` command (interaction:{interaction.id})")
