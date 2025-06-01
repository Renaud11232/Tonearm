import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import PlayerManager


class VoiceStateChangeListener(commands.Cog):

    def __init__(self, bot: commands.Bot, player_manager: PlayerManager):
        super().__init__()
        self.__bot = bot
        self.__player_manager = player_manager

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        player = self.__player_manager.get_player(member.guild)
        if before.channel is not None:
            if member.id == self.__bot.user.id:
                if after.channel is not None and before.channel != after.channel:
                    await player.on_bot_moved()
                elif after.channel is None:
                    await player.on_bot_disconnected()
            elif before.channel != after.channel:
                await player.on_user_moved(before.channel)
