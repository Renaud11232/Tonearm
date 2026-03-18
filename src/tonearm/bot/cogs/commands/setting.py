import logging

import discord
from discord import app_commands

from injector import singleton, inject, Injector

from tonearm.bot.managers import StorageManager, EmbedManager
from tonearm.bot.cogs.checks import is_guild_administrator
from tonearm.bot.cogs.transformers import BooleanTransformer, LocaleTransformer

from .base import CogBase


@singleton
class SettingCommand(CogBase):

    setting = app_commands.Group(
        name="setting",
        description="Manage global bot settings",
        allowed_contexts=app_commands.AppCommandContext(
            guild=True,
            dm_channel=False,
            private_channel=False
        )
    )
    setting_set = app_commands.Group(
        name="set",
        description="Set global bot settings",
        parent=setting
    )
    setting_reset = app_commands.Group(
        name="reset",
        description="Reset global bot settings",
        parent=setting
    )

    @inject
    def __init__(self,
                 storage_manager: StorageManager,
                 embed_manager: EmbedManager,
                 injector: Injector):
        super().__init__(injector)
        self.__storage_manager = storage_manager
        self.__embed_manager = embed_manager
        self.__logger = logging.getLogger("tonearm.commands")

    @setting_set.command(
        name="channel",
        description="Set the text channel where this bot should be used"
    )
    @app_commands.describe(
        value="Text channel where this bot should be used"
    )
    @is_guild_administrator()
    async def setting_set_channel(self,
                                  interaction: discord.Interaction,
                                  value: discord.TextChannel):
        self.__logger.debug(f"Handling `setting set channel` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_channel(value)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("channel", value)
        )
        self.__logger.debug(f"Successfully handled `setting set channel` command (interaction:{interaction.id})")

    @setting_set.command(
        name="anarchy",
        description="Enable anarchy mode, allowing everyone to use DJ commands"
    )
    @app_commands.describe(
        value="True to enable anarchy mode, False to disable it"
    )
    @is_guild_administrator()
    async def setting_set_anarchy(self,
                                  interaction: discord.Interaction,
                                  value: app_commands.Transform[bool, BooleanTransformer]):
        self.__logger.debug(f"Handling `setting set anarchy` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_anarchy(value)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("anarchy", value)
        )
        self.__logger.debug(f"Successfully handled `setting set channel` command (interaction:{interaction.id})")

    @setting_set.command(
        name="announcements",
        description="Enable automatic track announcements"
    )
    @app_commands.describe(
        value="True to enable automatic track announcements, False to disable them"
    )
    @is_guild_administrator()
    async def setting_set_announcements(self,
                                        interaction: discord.Interaction,
                                        value: app_commands.Transform[bool, BooleanTransformer]):
        self.__logger.debug(f"Handling `setting set announcements` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_announcements(value)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("announcements", value)
        )
        self.__logger.debug(f"Successfully handled `setting set announcements` command (interaction:{interaction.id})")

    @setting_set.command(
        name="locale",
        description="Set the language to use on this server"
    )
    @app_commands.describe(
        value="Language to use on this server"
    )
    @is_guild_administrator()
    async def setting_set_locale(self,
                                 interaction: discord.Interaction,
                                 value: app_commands.Transform[discord.Locale, LocaleTransformer]):
        self.__logger.debug(f"Handling `setting set locale` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_locale(value)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("locale", value)
        )
        self.__logger.debug(f"Successfully handled `setting set locale` command (interaction:{interaction.id})")

    @setting_reset.command(
        name="channel",
        description="Reset the text channel where this bot should be used"
    )
    @is_guild_administrator()
    async def setting_reset_channel(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `setting reset channel` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_channel(None)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_reset("channel", None)
        )
        self.__logger.debug(f"Successfully handled `setting reset channel` command (interaction:{interaction.id})")

    @setting_reset.command(
        name="anarchy",
        description="Reset anarchy mode, enabling back DJ enforcement"
    )
    @is_guild_administrator()
    async def setting_reset_anarchy(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `setting reset anarchy` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_anarchy(False)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_reset("anarchy", False)
        )
        self.__logger.debug(f"Successfully handled `setting reset channel` command (interaction:{interaction.id})")

    @setting_reset.command(
        name="announcements",
        description="Reset automatic track announcements, disabling them"
    )
    @is_guild_administrator()
    async def setting_reset_announcements(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `setting reset announcements` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_announcements(False)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("announcements", False)
        )
        self.__logger.debug(f"Successfully handled `setting reset announcements` command (interaction:{interaction.id})")

    @setting_reset.command(
        name="locale",
        description="Reset the language to use on this server"
    )
    @is_guild_administrator()
    async def setting_reset_locale(self, interaction: discord.Interaction):
        self.__logger.debug(f"Handling `setting reset locale` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_locale(discord.Locale.american_english)
        await interaction.followup.send(
            embed=self.__embed_manager.get(interaction.guild).setting_set("locale", discord.Locale.american_english)
        )
        self.__logger.debug(f"Successfully handled `setting reset locale` command (interaction:{interaction.id})")