import logging

import nextcord
from nextcord import SlashOption
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.managers import StorageManager
from tonearm.bot.services import EmbedService
from tonearm.bot.cogs.checks import IsGuildAdministrator

from .base import CommandCogBase


@singleton
class SettingCommand(CommandCogBase):

    @inject
    def __init__(self,
                 storage_manager: StorageManager,
                 embed_service: EmbedService,
                 is_guild_administrator: IsGuildAdministrator):
        super().__init__()
        self.__storage_manager = storage_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")
        self._add_checks(
            self.setting_set_channel,
            self.setting_set_anarchy,
            self.setting_set_announcements,
            self.setting_reset_channel,
            self.setting_reset_anarchy,
            self.setting_reset_announcements,
            checks=[
                application_checks.guild_only(),
                is_guild_administrator()
            ]
        )

    @nextcord.slash_command(
        name="setting",
        description="Manages various bot settings"
    )
    async def setting(self, interaction: nextcord.Interaction):
        pass

    @setting.subcommand(
        name="set",
        description="Sets the value of settings"
    )
    async def setting_set(self, interaction: nextcord.Interaction):
        pass

    @setting_set.subcommand(
        name="channel",
        description="Sets the text channel where this bot should be used"
    )
    async def setting_set_channel(self,
                                  interaction: nextcord.Interaction,
                                  channel: nextcord.TextChannel = SlashOption(
                                      name="channel",
                                      description="Text channel where this bot should be used",
                                      required=True
                                  )):
        self.__logger.debug(f"Handling `setting set channel` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_channel(channel) # type: ignore
        await interaction.followup.send(
            embed=self.__embed_service.setting_set("channel", channel)
        )
        self.__logger.debug(f"Successfully handled `setting set channel` command (interaction:{interaction.id})")

    @setting_set.subcommand(
        name="anarchy",
        description="Disables DJ enforcement if set to true, allowing everyone to use DJ commands"
    )
    async def setting_set_anarchy(self, interaction: nextcord.Interaction, value: bool):
        self.__logger.debug(f"Handling `setting set anarchy` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_anarchy(value)
        await interaction.followup.send(
            embed=self.__embed_service.setting_set("anarchy", value)
        )
        self.__logger.debug(f"Successfully handled `setting set channel` command (interaction:{interaction.id})")

    @setting_set.subcommand(
        name="announcements",
        description="Enables automatic track announcements"
    )
    async def setting_set_announcements(self, interaction: nextcord.Interaction, value: bool):
        self.__logger.debug(f"Handling `setting set announcements` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_announcements(value)
        await interaction.followup.send(
            embed=self.__embed_service.setting_set("announcements", value)
        )
        self.__logger.debug(f"Successfully handled `setting set announcements` command (interaction:{interaction.id})")

    @setting.subcommand(
        name="reset",
        description="Resets a setting to its default value"
    )
    async def setting_reset(self, interaction: nextcord.Interaction):
        pass

    @setting_reset.subcommand(
        name="channel",
        description="Resets the text channel where this bot should be used"
    )
    async def setting_reset_channel(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset channel` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_channel(None)
        await interaction.followup.send(
            embed=self.__embed_service.setting_reset("channel", None)
        )
        self.__logger.debug(f"Successfully handled `setting reset channel` command (interaction:{interaction.id})")

    @setting_reset.subcommand(
        name="anarchy",
        description="Resets anarchy mode, enabling back DJ enforcement"
    )
    async def setting_reset_anarchy(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset anarchy` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_anarchy(False)
        await interaction.followup.send(
            embed=self.__embed_service.setting_reset("anarchy", False)
        )
        self.__logger.debug(f"Successfully handled `setting reset channel` command (interaction:{interaction.id})")

    @setting_reset.subcommand(
        name="announcements",
        description="Resets automatic track announcements, disabling them"
    )
    async def setting_reset_announcements(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset announcements` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_announcements(False)
        await interaction.followup.send(
            embed=self.__embed_service.setting_set("announcements", False)
        )
        self.__logger.debug(f"Successfully handled `setting reset announcements` command (interaction:{interaction.id})")