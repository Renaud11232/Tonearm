from tonearm.bot.cogs import *

import nextcord
from nextcord.ext import commands

from injector import Module, singleton, provider


class BotModule(Module):

    @singleton
    @provider
    def provide_bot(self,
                    application_command_error_listener: ApplicationCommandErrorListener,
                    error_listener: ErrorListener,
                    ready_listener: ReadyListener,
                    voice_state_change_listener: VoiceStateChangeListener,
                    back_command: BackCommand,
                    clean_command: CleanCommand,
                    clear_command: ClearCommand,
                    debug_command: DebugCommand,
                    dj_command: DjCommand,
                    forward_command: ForwardCommand,
                    history_command: HistoryCommand,
                    join_command: JoinCommand,
                    jump_command: JumpCommand,
                    leave_command: LeaveCommand,
                    loop_command: LoopCommand,
                    move_command: MoveCommand,
                    next_command: NextCommand,
                    now_command: NowCommand,
                    pause_command: PauseCommand,
                    play_command: PlayCommand,
                    previous_command: PreviousCommand,
                    queue_command: QueueCommand,
                    remove_command: RemoveCommand,
                    resume_command: ResumeCommand,
                    rewind_command: RewindCommand,
                    seek_command: SeekCommand,
                    setting_command: SettingCommand,
                    shuffle_command: ShuffleCommand,
                    shutdown_command: ShutdownCommand,
                    stop_command: StopCommand,
                    version_command: VersionCommand,
                    volume_command: VolumeCommand,
                    votenext_command: VotenextCommand) -> commands.Bot:
        intents = nextcord.Intents.default()
        intents.members = True #Needed to check dj members
        intents.voice_states = True #Needed to check when members leave voice channels
        activity = nextcord.Activity(
            type=nextcord.ActivityType.listening,
            name="/play"
        )
        bot = commands.Bot(
            intents=intents,
            activity=activity
        )
        bot.add_cog(application_command_error_listener)
        bot.add_cog(error_listener)
        bot.add_cog(ready_listener)
        bot.add_cog(voice_state_change_listener)
        bot.add_cog(back_command)
        bot.add_cog(clean_command)
        bot.add_cog(clear_command)
        bot.add_cog(debug_command)
        bot.add_cog(dj_command)
        bot.add_cog(forward_command)
        bot.add_cog(history_command)
        bot.add_cog(join_command)
        bot.add_cog(jump_command)
        bot.add_cog(leave_command)
        bot.add_cog(loop_command)
        bot.add_cog(move_command)
        bot.add_cog(next_command)
        bot.add_cog(now_command)
        bot.add_cog(pause_command)
        bot.add_cog(play_command)
        bot.add_cog(previous_command)
        bot.add_cog(queue_command)
        bot.add_cog(remove_command)
        bot.add_cog(resume_command)
        bot.add_cog(rewind_command)
        bot.add_cog(seek_command)
        bot.add_cog(setting_command)
        bot.add_cog(shuffle_command)
        bot.add_cog(shutdown_command)
        bot.add_cog(stop_command)
        bot.add_cog(version_command)
        bot.add_cog(volume_command)
        bot.add_cog(votenext_command)
        @bot.event
        async def on_application_command_error(interaction: nextcord.Interaction, error):
            await application_command_error_listener.on_application_command_error(interaction, error)
        @bot.event
        async def on_error(event: str, *args, **kwargs):
            await error_listener.on_error(event, *args, **kwargs)
        return bot
