import logging

import nextcord
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
        self._add_checks(self.set_channel, self.set_anarchy, self.reset_channel, self.reset_anarchy, checks=[
            application_checks.guild_only(),
            is_guild_administrator()
        ])

    @nextcord.slash_command(
        description="Manages various bot settings"
    )
    async def setting(self, interaction: nextcord.Interaction):
        pass

    @setting.subcommand(
        description="Sets the value of settings"
    )
    async def set(self, interaction: nextcord.Interaction):
        pass

    @set.subcommand(
        description="Sets the text channel where this bot should be used to the current channel",
        name="channel"
    )
    async def set_channel(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting set channel` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_channel(interaction.channel)
        await interaction.followup.send(
            embed=self.__embed_service.setting_set("channel", interaction.channel)
        )
        self.__logger.debug(f"Successfully handled `setting set channel` command (interaction:{interaction.id})")

    @set.subcommand(
        description="Disables DJ enforcement if enabled, allowing everyone to use most commands",
        name="anarchy"
    )
    async def set_anarchy(self, interaction: nextcord.Interaction, value: bool):
        self.__logger.debug(f"Handling `setting set anarchy` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_anarchy(value)
        await interaction.followup.send(
            embed=self.__embed_service.setting_set("anarchy", value)
        )
        self.__logger.debug(f"Successfully handled `setting set channel` command (interaction:{interaction.id})")

    @setting.subcommand(
        description="Resets a setting to its default value"
    )
    async def reset(self, interaction: nextcord.Interaction):
        pass

    @reset.subcommand(
        description="Resets the text channel where this bot should be used",
        name="channel"
    )
    async def reset_channel(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset channel` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_channel(None)
        await interaction.followup.send(
            embed=self.__embed_service.setting_reset("channel", None)
        )
        self.__logger.debug(f"Successfully handled `setting reset channel` command (interaction:{interaction.id})")

    @reset.subcommand(
        description="Resets anarchy mode, enabling back DJ enforcement",
        name="anarchy"
    )
    async def reset_anarchy(self, interaction: nextcord.Interaction):
        self.__logger.debug(f"Handling `setting reset anarchy` command (interaction:{interaction.id})")
        await interaction.response.defer()
        self.__storage_manager.get(interaction.guild).set_anarchy(False)
        await interaction.followup.send(
            embed=self.__embed_service.setting_reset("anarchy", False)
        )
        self.__logger.debug(f"Successfully handled `setting reset channel` command (interaction:{interaction.id})")