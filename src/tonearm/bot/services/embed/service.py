import math
from typing import List, Any

import nextcord
from injector import singleton

from tonearm.bot.services.player.status import PlayerStatus
from tonearm.bot.services.player.track import QueuedTrack
from tonearm.bot.services.player.loop import LoopMode
from tonearm.bot.services.bot import TonearmVersion
from tonearm.utils.markdown import *
from tonearm.utils.strings import *

from .exceptions import EmbedException


@singleton
class EmbedService:

    @staticmethod
    def error(e):
        return nextcord.Embed(
            description=f":x: {escape_markdown(str(e))}",
            colour=nextcord.Colour.red()
        )

    @staticmethod
    def back(track: int):
        if track == 1:
            return EmbedService.previous()
        return nextcord.Embed(
            description=f":track_previous: Rewinding to track {track + 1}. Let’s bring it back!",
            colour=nextcord.Colour.dark_purple()
        )


    @staticmethod
    def clean(messages: List[nextcord.Message]):
        return nextcord.Embed(
            description=f":ghost: All my {len(messages)} message(s) are gone. It's like I was never here !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def clear():
        return nextcord.Embed(
            description=":broom: Wiped the queue. Sometimes starting fresh hits different.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def dj_add(role_or_member: nextcord.Role | nextcord.Member):
        return nextcord.Embed(
            description=f":white_check_mark: Promoted {role_or_member.mention} to DJ. Don’t scratch the vinyl !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def dj_remove(role_or_member: nextcord.Role | nextcord.Member):
        return nextcord.Embed(
            description=f":white_check_mark: {role_or_member.mention} is off the decks for now.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def forward():
        return nextcord.Embed(
            description=":fast_forward: Who needs intros anyway ?",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def history(previous_tracks: List[QueuedTrack], page: int):
        embed = nextcord.Embed(
            title="History",
            colour=nextcord.Colour.dark_purple()
        )
        EmbedService.__build_track_list(embed, previous_tracks, page, "Previous tracks :", "Played")
        return embed

    @staticmethod
    def join():
        return nextcord.Embed(
            description=":party_popper: Let's get this party started !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def jump(track: int):
        if track == 0:
            return EmbedService.next()
        return nextcord.Embed(
            description=f":track_next: Boom. Skipped straight to track {track + 1}. Enjoy !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def leave():
        return nextcord.Embed(
            description=":microphone: Mic dropped. I'm gone.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def loop(mode: LoopMode):
        embed = nextcord.Embed(
            colour=nextcord.Colour.dark_purple()
        )
        if mode == LoopMode.OFF:
            embed.description = ":arrow_right: Looping turned off. One play, no reruns."
        elif mode == LoopMode.TRACK:
            embed.description = ":repeat_one: You must really love this one. Looping it on repeat."
        else:
            embed.description = ":repeat: Get ready for the encore. And the encore's encore. Looping the queue !"
        return embed

    @staticmethod
    def move(track: QueuedTrack, fr0m: int, to: int):
        return nextcord.Embed(
            description=f":ninja: Shifted {bold(escape_markdown(track.title))} like a playlist ninja. Moved from {fr0m + 1} to {to + 1}.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def next():
        return nextcord.Embed(
            description=":track_next: Skipping the current track, I didn't like this one either.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def __slice_duration(duration):
        if math.isinf(duration):
            return math.nan, math.nan, math.nan, math.nan
        total_seconds = math.floor(duration / 1000)
        seconds = total_seconds % 60
        minutes = (total_seconds // 60) % 60
        hours = (total_seconds // (60 * 60)) % 24
        days = total_seconds // (60 * 60 *  24)
        return days, hours, minutes, seconds

    @staticmethod
    def __format_duration(elapsed, total, minimum_positions):
        elapsed_days, elapsed_hours, elapsed_minutes, elapsed_seconds = EmbedService.__slice_duration(elapsed)
        total_days, total_hours, total_minutes, total_seconds = EmbedService.__slice_duration(total)
        elapsed_segments = []
        total_segments = []
        show_next_number = False
        if elapsed_days > 0 or total_days > 0 or minimum_positions > 3:
            elapsed_segments.append(f"{elapsed_days}")
            total_segments.append("--" if math.isnan(total_days) else f"{total_days}")
            show_next_number = True
        if show_next_number or elapsed_hours > 0 or total_hours > 0 or minimum_positions > 2:
            elapsed_segments.append(f"{elapsed_hours:0>2}")
            total_segments.append("--" if math.isnan(total_hours) else f"{total_hours:0>2}")
            show_next_number = True
        if show_next_number or elapsed_minutes > 0 or total_minutes > 0 or minimum_positions > 1:
            elapsed_segments.append(f"{elapsed_minutes:0>2}")
            total_segments.append("--" if math.isnan(total_minutes) else f"{total_minutes:0>2}")
            show_next_number = True
        if show_next_number or elapsed_seconds > 0 or total_seconds > 0 or minimum_positions > 0:
            elapsed_segments.append(f"{elapsed_seconds:0>2}")
            total_segments.append("--" if math.isnan(total_seconds) else f"{total_seconds:0>2}")
        return ":".join(elapsed_segments), ":".join(total_segments)

    @staticmethod
    def now(player_status: PlayerStatus):
        elapsed_fraction = round((player_status.audio_source.elapsed / player_status.audio_source.total) * 9)
        bar_progress = "".join([":radio_button:" if i == elapsed_fraction else "▬" for i in range(10)])
        elapsed_time, total_time = EmbedService.__format_duration(
            player_status.audio_source.elapsed,
            player_status.audio_source.total,
            minimum_positions=2
        )
        status_icon = ":pause_button:" if player_status.audio_source.paused else ":arrow_forward:"
        loop_icon = {
            LoopMode.OFF.name: ":arrow_right:",
            LoopMode.TRACK.name: ":repeat_one:",
            LoopMode.QUEUE.name: ":repeat:"
        }[player_status.queue.loop_mode.name]
        embed = nextcord.Embed(
            title="Now Playing",
            description=(
                f"{bold(link(escape_link_text(truncate(player_status.queue.current_track.title, 50)), escape_link_url(player_status.queue.current_track.url)))}\n"
                f"Requested by : {player_status.queue.current_track.member.mention}\n"
                f"\n"
                f"{status_icon} {bar_progress} {inline_code(f'[{elapsed_time}/{total_time}]')} {loop_icon} :sound: {round(player_status.audio_source.volume)}%"
            ),
            colour=nextcord.Colour.dark_purple()
        )
        embed.set_thumbnail(url=player_status.queue.current_track.thumbnail)
        embed.set_footer(
            text=f"Source : {escape_markdown(player_status.queue.current_track.source)}"
        )
        return embed

    @staticmethod
    def pause():
        return nextcord.Embed(
            description=":pause_button: Playback paused. Take your time !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def play(tracks: List[QueuedTrack]):
        embed = nextcord.Embed(
                colour=nextcord.Colour.dark_purple()
            )
        if len(tracks) > 1:
            embed.description = f":cd: Added {bold(f'{len(tracks)} tracks')} to the queue! Now that’s what I call a playlist."
        else:
            embed.description = f":cd: Added {bold(escape_markdown(tracks[0].title))} to the queue ! This one’s gonna slap."
        return embed

    @staticmethod
    def previous():
        return nextcord.Embed(
            description=":track_previous: Because one listen wasn’t enough...",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def __build_track_list(embed: nextcord.Embed, tracks: List[QueuedTrack], page: int, title: str, title2: str):
        if len(tracks) == 0:
            max_pages = 1
        else:
            max_pages = math.ceil(len(tracks) / 10)
        if page >= max_pages:
            raise EmbedException(f"I can't show you page {page + 1} out of {max_pages}")
        if len(tracks) == 0:
            track_list = [
                italic("Nothing to show here")
            ]
        else:
            tracks_chunk = tracks[page * 10: page * 10 + 10]
            track_list = [
                f"{bold(f'{page * 10 + track + 1}.')} {link(escape_link_text(truncate(tracks_chunk[track].title, 25)), escape_link_url(tracks_chunk[track].url))}"
                for track in range(len(tracks_chunk))
            ]
        embed.add_field(
            name=title,
            value="\n".join(track_list),
            inline=False
        )
        embed.add_field(
            name=title2,
            value=f"{len(tracks)} tracks" if len(tracks) > 1 else f"{len(tracks)} track",
            inline=True
        )
        embed.add_field(
            name="Page",
            value=f"{page + 1} out of {max_pages}",
            inline=True
        )

    @staticmethod
    def queue(player_status: PlayerStatus, page: int):
        embed = EmbedService.now(player_status)
        EmbedService.__build_track_list(embed, player_status.queue.next_tracks, page, "Up next :", "In queue")
        return embed

    @staticmethod
    def remove(track: QueuedTrack):
        return nextcord.Embed(
            description=f":scissors: Say goodbye to {bold(escape_markdown(track.title))}. It didn’t make the cut.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def resume():
        return nextcord.Embed(
            description=":play_pause: Back in action ! Enjoy the tracks.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def rewind():
        return nextcord.Embed(
            description=":rewind: That part was worth a second listen !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def seek():
        return nextcord.Embed(
            description=":dart: Dropping the needle, classic move.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def __setting_repr(value: Any) -> str:
        if hasattr(value, "mention"):
            return value.mention
        return inline_code(escape_markdown(repr(value)))

    @staticmethod
    def setting_set(name: str, value: Any):
        return nextcord.Embed(
            description=f":tools: All set! {inline_code(escape_markdown(name))} is now {EmbedService.__setting_repr(value)}.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def setting_reset(name: str, value: Any):
        return nextcord.Embed(
            description=f":tools: Boom ! {inline_code(escape_markdown(name))} is back to default: {EmbedService.__setting_repr(value)}.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def shuffle():
        return nextcord.Embed(
            description=":twisted_rightwards_arrows: Shuffled the queue. I hope you like surprises !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def shutdown():
        return nextcord.Embed(
            description=":saluting_face: Initiating shutdown sequence... it’s been an honor.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def stop():
        return nextcord.Embed(
            description=":stop_button: Music stopped. The crowd goes silent.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def version(version: TonearmVersion):
        return nextcord.Embed(
            description=(
                f":robot: {link('Tonearm', version.homepage)}\n"
                f"\n"
                f"Version {inline_code(f'v{version.version}')}, up and running !\n"
                f"Crafted with :heart: by {', '.join(map(italic, version.authors))}."
            ),
            colour=nextcord.Colour.dark_purple(),
        )

    @staticmethod
    def volume(volume: int):
        return nextcord.Embed(
            description=f":sound: Volume’s now {volume}%. Don’t blame me if it’s too loud !",
            colour=nextcord.Colour.dark_purple()
        )