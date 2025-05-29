import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import QueueManager
from tonearm.exceptions import TonearmException

class LeaveCommand(commands.Cog):

    def __init__(self, bot: commands.Bot, queue_manager: QueueManager):
        self.__bot = bot
        self.__queue_manager = queue_manager

    @nextcord.slash_command(
        description="Leaves the current voice channel"
    )
    async def leave(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        queue = self.__queue_manager.get_queue(interaction.guild)
        try:
            await queue.leave(interaction.user.voice)
            await interaction.followup.send(f":wave: Goodbye !")
        except TonearmException as e:
            await interaction.followup.send(f":x: {str(e)}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        if before.channel is not None and before.channel != after.channel:
            same_voice_channel = False
            alone = True
            for member in before.channel.members:
                if member.id == self.__bot.user.id:
                    same_voice_channel = True
                else:
                    alone = False
            if same_voice_channel and alone:
                queue = self.__queue_manager.get_queue(member.guild)
                await queue.leave(before)