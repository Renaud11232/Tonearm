import nextcord
from nextcord.ext import application_checks

from injector import singleton, inject

from tonearm.bot.cogs.checks import IsCorrectChannel, IsNotAnarchy

from .base import CommandCogBase


@singleton
class VotenextCommand(CommandCogBase):

    @inject
    def __init__(self, is_correct_channel: IsCorrectChannel, is_not_anarchy: IsNotAnarchy):
        super().__init__()
        self._add_checks(self.votenext, self.voteskip, checks=[
            application_checks.guild_only(),
            is_correct_channel(),
            is_not_anarchy()
        ])

    @nextcord.slash_command(
        name="votenext",
        description="Votes to skip the current track"
    )
    async def votenext(self, interaction: nextcord.Interaction):
        await self.__votenext(interaction)

    @nextcord.slash_command(
        name="voteskip",
        description="Votes to skip the current track"
    )
    async def voteskip(self, interaction: nextcord.Interaction):
        await self.__votenext(interaction)

    async def __votenext(self, interaction: nextcord.Interaction):
        #TODO :ballot_box: We need Y - X more votes to skip this track.
        #TODO :track_next: Track skipped by popular demand!
        #TODO :x: You already voted to skip this track.
        await interaction.send(":wrench: This feature is not implemented yet !")
