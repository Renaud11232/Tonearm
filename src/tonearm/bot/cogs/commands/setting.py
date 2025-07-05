import logging

import nextcord
from nextcord import SlashOption, Locale
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.managers import StorageManager, TranslationsManager, EmbedManager
from tonearm.bot.cogs.checks import IsGuildAdministrator
from tonearm.bot.cogs.converters import BooleanConverter, LocaleConverter

from .base import CommandCogBase


@singleton
class SettingCommand(CommandCogBase):

    @inject
    def __init__(self,
                 storage_manager: StorageManager,
                 embed_manager: EmbedManager,
                 is_guild_administrator: IsGuildAdministrator):
        super().__init__()
        self.__storage_manager = storage_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(
            self.setting_set_channel,
            self.setting_set_anarchy,
            self.setting_set_announcements,
            self.setting_set_locale,
            self.setting_reset_channel,
            self.setting_reset_anarchy,
            self.setting_reset_announcements,
            self.setting_reset_locale,
            checks=[
                application_checks.guild_only(),
                is_guild_administrator()
            ]
        )

    @nextcord.slash_command(
        name="setting"
    )
    async def setting(self, interaction: nextcord.Interaction):
        pass

    @setting.subcommand(
        name="set"
    )
    async def setting_set(self, interaction: nextcord.Interaction):
        pass

    @setting_set.subcommand(
        name="channel",
        description=TranslationsManager().get(Locale.en_US).gettext("Set the text channel where this bot should be used"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Set the text channel where this bot should be used"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Set the text channel where this bot should be used"),
        }
    )
    async def setting_set_channel(self,
                                  interaction: nextcord.Interaction,
                                  value: nextcord.TextChannel = SlashOption(
                                      name=TranslationsManager().get(Locale.en_US).gettext("value"),
                                      name_localizations={
                                          Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("value"),
                                          Locale.fr: TranslationsManager().get(Locale.fr).gettext("value"),
                                      },
                                      description=TranslationsManager().get(Locale.en_US).gettext("Text channel where this bot should be used"),
                                      description_localizations={
                                          Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Text channel where this bot should be used"),
                                          Locale.fr: TranslationsManager().get(Locale.fr).gettext("Text channel where this bot should be used"),
                                      },
                                      required=True
                                  )):
        self.__logger.debug(f"Handling `setting set channel` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_channel(channel) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("channel", value)
        )
        self.__logger.debug(f"Successfully handled `setting set channel` command (interaction:{interaction.id})")

    @setting_set.subcommand(
        name="anarchy",
        description=TranslationsManager().get(Locale.en_US).gettext("Enable anarchy mode, allowing everyone to use DJ commands"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Enable anarchy mode, allowing everyone to use DJ commands"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Enable anarchy mode, allowing everyone to use DJ commands"),
        }
    )
    async def setting_set_anarchy(self,
                                  interaction: nextcord.Interaction,
                                  value: BooleanConverter = SlashOption(
                                      name=TranslationsManager().get(Locale.en_US).gettext("value"),
                                      name_localizations={
                                          Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("value"),
                                          Locale.fr: TranslationsManager().get(Locale.fr).gettext("value"),
                                      },
                                      description=TranslationsManager().get(Locale.en_US).gettext("True to enable anarchy mode, False to disable it"),
                                      description_localizations={
                                          Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("True to enable anarchy mode, False to disable it"),
                                          Locale.fr: TranslationsManager().get(Locale.fr).gettext("True to enable anarchy mode, False to disable it")
                                      },
                                      choices=BooleanConverter.get_choices(),
                                      choice_localizations=BooleanConverter.get_choice_localizations(),
                                      required=True
                                  )):
        self.__logger.debug(f"Handling `setting set anarchy` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_anarchy(value)  # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("anarchy", value)
        )
        self.__logger.debug(f"Successfully handled `setting set channel` command (interaction:{interaction.id})")

    @setting_set.subcommand(
        name="announcements",
        description=TranslationsManager().get(Locale.en_US).gettext("Enable automatic track announcements"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Enable automatic track announcements"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Enable automatic track announcements"),
        }
    )
    async def setting_set_announcements(self,
                                        interaction: nextcord.Interaction,
                                        value: BooleanConverter = SlashOption(
                                            name=TranslationsManager().get(Locale.en_US).gettext("value"),
                                            name_localizations={
                                                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("value"),
                                                Locale.fr: TranslationsManager().get(Locale.fr).gettext("value"),
                                            },
                                            description=TranslationsManager().get(Locale.en_US).gettext("True to enable automatic track announcements, False to disable them"),
                                            description_localizations={
                                                Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("True to enable automatic track announcements, False to disable them"),
                                                Locale.fr: TranslationsManager().get(Locale.fr).gettext("True to enable automatic track announcements, False to disable them")
                                            },
                                            choices=BooleanConverter.get_choices(),
                                            choice_localizations=BooleanConverter.get_choice_localizations(),
                                            required=True
                                  )):
        self.__logger.debug(f"Handling `setting set announcements` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_announcements(value)  # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("announcements", value)
        )
        self.__logger.debug(f"Successfully handled `setting set announcements` command (interaction:{interaction.id})")

    @setting_set.subcommand(
        name="locale",
        description=TranslationsManager().get(Locale.en_US).gettext("Set the language to use on this server"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Set the language to use on this server"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Set the language to use on this server"),
        }
    )
    async def setting_set_locale(self,
                                 interaction: nextcord.Interaction,
                                 value: LocaleConverter = SlashOption(
                                     name=TranslationsManager().get(Locale.en_US).gettext("value"),
                                     name_localizations={
                                         Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("value"),
                                         Locale.fr: TranslationsManager().get(Locale.fr).gettext("value"),
                                     },
                                     description=TranslationsManager().get(Locale.en_US).gettext("Language to use on this server"),
                                     description_localizations={
                                         Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Language to use on this server"),
                                         Locale.fr: TranslationsManager().get(Locale.fr).gettext("Language to use on this server")
                                     },
                                     choices=LocaleConverter.get_choices(),
                                     required=True
                                 )):
        self.__logger.debug(f"Handling `setting set locale` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_locale(value)  # type: ignore
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("locale", value)
        )
        self.__logger.debug(f"Successfully handled `setting set locale` command (interaction:{interaction.id})")

    @setting.subcommand(
        name="reset"
    )
    async def setting_reset(self, interaction: nextcord.Interaction):
        pass

    @setting_reset.subcommand(
        name="channel",
        description=TranslationsManager().get(Locale.en_US).gettext("Reset the text channel where this bot should be used"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Reset the text channel where this bot should be used"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Reset the text channel where this bot should be used"),
        }
    )
    async def setting_reset_channel(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset channel` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_channel(None)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_reset("channel", None)
        )
        self.__logger.debug(f"Successfully handled `setting reset channel` command (interaction:{interaction.id})")

    @setting_reset.subcommand(
        name="anarchy",
        description=TranslationsManager().get(Locale.en_US).gettext("Reset anarchy mode, enabling back DJ enforcement"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Reset anarchy mode, enabling back DJ enforcement"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Reset anarchy mode, enabling back DJ enforcement"),
        }
    )
    async def setting_reset_anarchy(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset anarchy` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_anarchy(False)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_reset("anarchy", False)
        )
        self.__logger.debug(f"Successfully handled `setting reset channel` command (interaction:{interaction.id})")

    @setting_reset.subcommand(
        name="announcements",
        description=TranslationsManager().get(Locale.en_US).gettext("Reset automatic track announcements, disabling them"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Reset automatic track announcements, disabling them"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Reset automatic track announcements, disabling them"),
        }
    )
    async def setting_reset_announcements(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset announcements` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_announcements(False)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("announcements", False)
        )
        self.__logger.debug(f"Successfully handled `setting reset announcements` command (interaction:{interaction.id})")

    @setting_reset.subcommand(
        name="locale",
        description=TranslationsManager().get(Locale.en_US).gettext("Reset the language to use on this server"),
        description_localizations={
            Locale.en_US: TranslationsManager().get(Locale.en_US).gettext("Reset the language to use on this server"),
            Locale.fr: TranslationsManager().get(Locale.fr).gettext("Reset the language to use on this server"),
        }
    )
    async def setting_reset_locale(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset locale` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_locale(nextcord.Locale.en_US)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("locale", nextcord.Locale.en_US)
        )
        self.__logger.debug(f"Successfully handled `setting reset locale` command (interaction:{interaction.id})")