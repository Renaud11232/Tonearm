import logging

import nextcord
from nextcord.ext import commands

from injector import singleton, inject

from tonearm.bot.managers import StorageManager
from tonearm.bot.services import EmbedService


@singleton
class SettingCommand(commands.Cog):

    @inject
    def __init__(self, storage_manager: StorageManager, embed_service: EmbedService):
        super().__init__()
        self.__storage_manager = storage_manager
        self.__embed_service = embed_service
        self.__logger = logging.getLogger("tonearm.commands")

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
        description="Sets the text channel where this bot should be used",
        name="channel"
    )
    async def set_channel(self, interaction: nextcord.Interaction, value: nextcord.TextChannel):
        #TODO
        pass

    @set.subcommand(
        description="Disables DJ enforcement if enabled, allowing everyone to use most commands",
        name="anarchy"
    )
    async def set_anarchy(self, interaction: nextcord.Interaction, value: bool):
        #TODO
        pass

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
        pass
        #TODO

    @reset.subcommand(
        description="Resets anarchy mode, enabling back DJ enforcement",
        name="anarchy"
    )
    async def reset_anarchy(self, interaction: nextcord.Interaction):
        pass
        #TODO