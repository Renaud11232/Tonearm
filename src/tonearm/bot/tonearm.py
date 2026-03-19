from tonearm.bot.cogs import *

from injector import singleton, inject

import discord
from discord import app_commands
from discord.ext import commands

from tonearm.configuration import Configuration

from .translator import TonearmTranslator


@singleton
class TonearmBot(commands.Bot):

    @inject
    def __init__(self,
                 configuration: Configuration,
                 translator: TonearmTranslator,
                 ready_listener: ReadyListener,
                 voice_state_change_listener: VoiceStateChangeListener,
                 app_command_error_listener: AppCommandErrorListener,
                 back_command: BackCommand,
                 clean_command: CleanCommand,
                 clear_command: ClearCommand,
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
                 votenext_command: VotenextCommand):
        intents = discord.Intents.default()
        intents.members = True
        intents.voice_states = True
        activity = discord.Activity(
            type=configuration.activity_type,
            name=configuration.activity_name,
            state=configuration.activity_state,
            url=configuration.activity_url
        )
        super().__init__(
            status=configuration.status,
            intents=intents,
            activity=activity,
            command_prefix=[],
            help_command=None
        )
        self.__tonearm_translator = translator
        self.__app_command_error_listener = app_command_error_listener
        self.__tonearm_cogs = [
            ready_listener,
            voice_state_change_listener,
            back_command,
            clean_command,
            clear_command,
            dj_command,
            forward_command,
            history_command,
            join_command,
            jump_command,
            leave_command,
            loop_command,
            move_command,
            next_command,
            now_command,
            pause_command,
            play_command,
            previous_command,
            queue_command,
            remove_command,
            resume_command,
            rewind_command,
            seek_command,
            setting_command,
            shuffle_command,
            shutdown_command,
            stop_command,
            version_command,
            volume_command,
            votenext_command
        ]

    async def setup_hook(self) -> None:
        await self.tree.set_translator(self.__tonearm_translator)
        for cog in self.__tonearm_cogs:
            await self.add_cog(cog)
        @self.tree.error
        async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
            await self.__app_command_error_listener.on_app_command_error(interaction, error)
        await self.tree.sync()
