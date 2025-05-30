import nextcord
from nextcord.ext import commands

from tonearm.bot.managers import PlayerManager


class VoiceStateChangeListener(commands.Cog):

    def __init__(self, bot: commands.Bot, player_manager: PlayerManager):
        super().__init__()
        self.__bot = bot
        self.__player_manager = player_manager

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
    #     guild = member.guild
    #     if guild.voice_client is None or guild.voice_client.channel or before.channel is None:
    #         print(guild.voice_client)
    #         print(guild.voice_client.channel)
    #         print(before.channel)
    #         return
    #     player = self.__player_manager.get_player(guild)
    #     if after.channel is None or before.channel != after.channel:
    #         if member == self.__bot.user:
    #             await player.stop()
    #         else:
    #             voice_channel = self.__bot.get_channel(guild.voice_client.channel.id)
    #             humans = [m for m in voice_channel.members if not m.bot]
    #             if len(humans) == 0:
    #                 await player.leave()
