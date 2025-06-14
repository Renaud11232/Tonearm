import math
from typing import List

import nextcord
from injector import singleton

from tonearm.bot.services.player import PlayerStatus, QueuedTrack
from tonearm.utils.markdown import *

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
    def clean():
        return nextcord.Embed(
            description=":ghost: All my messages are gone. It's like I was never here !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def clear():
        return nextcord.Embed(
            description=":broom: Wiped the queue. Sometimes starting fresh hits different.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def forward():
        return nextcord.Embed(
            description=":fast_forward: Who needs intros anyway ?",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def join():
        return nextcord.Embed(
            description=":party_popper: Let's get this party started !",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def leave():
        return nextcord.Embed(
            description=":microphone: Mic dropped. I'm gone.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def next():
        return nextcord.Embed(
            description=":track_next: Skipping the current track, I didn't like this one either.",
            colour=nextcord.Colour.dark_purple()
        )

    @staticmethod
    def __format_duration(duration, minimum_positions):
        if math.isinf(duration):
            return "∞"
        total_seconds = math.floor(duration / 1000)
        seconds = total_seconds % 60
        minutes = (total_seconds // 60) % 60
        hours = (total_seconds // (60 * 60)) % 24
        days = total_seconds // (60 * 60 *  24)
        positions = []
        show_next_number = False
        if days > 0 or minimum_positions > 3:
            positions.append(f"{days}")
            show_next_number = True
        if show_next_number or hours > 0 or minimum_positions > 2:
            positions.append(f"{hours:0>2}")
            show_next_number = True
        if show_next_number or minutes > 0 or minimum_positions > 1:
            positions.append(f"{minutes:0>2}")
            show_next_number = True
        if show_next_number or seconds > 0 or minimum_positions > 0:
            positions.append(f"{seconds:0>2}")
        return ":".join(positions)

    @staticmethod
    def now(player_status: PlayerStatus):
        elapsed_fraction = round((player_status.audio_source.elapsed / player_status.audio_source.total) * 9)
        bar_progress = "".join([":radio_button:" if i == elapsed_fraction else "▬" for i in range(10)])
        total_time = EmbedService.__format_duration(player_status.audio_source.total, minimum_positions=2)
        elapsed_time = EmbedService.__format_duration(
            player_status.audio_source.elapsed,
            minimum_positions=max(len(total_time.split(":")), 2)
        )
        embed = nextcord.Embed(
            title="Now Playing",
            description=(
                f"{bold(link(escape_link_text(player_status.queue.current_track.title), escape_link_url(player_status.queue.current_track.url)))}\n"
                f"Requested by : {player_status.queue.current_track.member.mention}\n"
                f"\n"
                f":arrow_forward: {bar_progress} {inline_code(f'[{elapsed_time}/{total_time}]')} :sound: {round(player_status.audio_source.volume)}%"
            ),
            colour=nextcord.Colour.dark_purple()
        )
        embed.set_thumbnail(url=player_status.queue.current_track.thumbnail)
        embed.set_footer(
            text=f"Source : {escape_markdown(player_status.queue.current_track.source)}"
        )
        return embed

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
    def queue(player_status: PlayerStatus, page: int):
        next_tracks = player_status.queue.next_tracks
        if len(next_tracks) == 0:
            max_pages = 1
        else:
            max_pages = math.ceil(len(next_tracks) / 10)
        if page > max_pages:
            raise EmbedException(f"Wow, the queue isn't that big.")
        if len(next_tracks) == 0:
            up_next = "*No track in the queue*"
        else:
            tracks = next_tracks[(page - 1) * 10: (page - 1) * 10 + 10]
            up_next = "\n".join([
                f"{bold(f'{track + 1}.')} {link(escape_link_text(f'{tracks[track].title[:25]}{"..." if len(tracks[track].title) > 25 else ""}'), escape_link_url(tracks[track].url))}" for track in range(len(tracks))
            ])
        embed = EmbedService.now(player_status)
        embed.add_field(
            name="Up next :",
            value=up_next,
            inline=False
        )
        embed.add_field(
            name="In queue",
            value=f"{len(next_tracks)} tracks" if len(next_tracks) > 1 else f"{len(next_tracks)} track",
            inline=True
        )
        embed.add_field(
            name="Page",
            value=f"{page} out of {max_pages}",
            inline=True
        )
        return embed

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
    def volume(volume: int):
        return nextcord.Embed(
            description=f":sound: Volume’s now {volume}%. Don’t blame me if it’s too loud !",
            colour=nextcord.Colour.dark_purple()
        )