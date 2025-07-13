import math
from typing import List, Any
from enum import Enum

import nextcord
from nextcord import Locale

from injector import inject, noninjectable

from tonearm.bot.exceptions import TonearmException
from tonearm.bot.services.player.status import PlayerStatus
from tonearm.bot.services.player.track import QueuedTrack
from tonearm.bot.services.player.loop import LoopMode
from tonearm.bot.services.player.vote import VoteStatus
from tonearm.bot.services.bot import TonearmVersion
from tonearm.bot.services.storage import StorageService
from tonearm.bot.managers.translations import TranslationsManager
from tonearm.configuration import Configuration
from tonearm.utils.markdown import *
from tonearm.utils.strings import *

from .exceptions import EmbedException


class EmbedService:

    @inject
    @noninjectable("storage_service")
    def __init__(self, storage_service: StorageService, configuration: Configuration):
        self.__storage_service = storage_service
        self.__configuration = configuration

    @property
    def __locale(self) -> Locale:
        return self.__storage_service.get_locale()

    def error(self, error: TonearmException):
        return self.error_message(error.template, **error.kwargs)

    def error_message(self, template: str, **kwargs) -> nextcord.Embed:
        message = TranslationsManager().get(self.__locale).gettext(template).format(**kwargs)
        return nextcord.Embed(
            description=f":x: {escape_markdown(message)}",
            colour=nextcord.Colour.red()
        )

    def back(self, track: int):
        if track == 1:
            return self.previous()
        message = TranslationsManager().get(self.__locale).gettext("Rewinding to track {track}. Let’s bring it back !").format(
            track=track + 1
        )
        return nextcord.Embed(
            description=f":track_previous: {message}",
            colour=self.__configuration.colour
        )


    def clean(self, messages: List[nextcord.Message]):
        len_messages = len(messages)
        message = TranslationsManager().get(self.__locale).ngettext(
            "My message is gone. It's like I was never here !",
            "My {len_messages} messages are gone. It's like I was never here !",
            len_messages
        ).format(
            len_messages=len_messages
        )
        return nextcord.Embed(
            description=f":ghost: {message}",
            colour=self.__configuration.colour
        )

    def clear(self):
        message = TranslationsManager().get(self.__locale).gettext("Wiped the queue. Sometimes starting fresh hits different.")
        return nextcord.Embed(
            description=f":broom: {message}",
            colour=self.__configuration.colour
        )

    def dj_add(self, role_or_member: nextcord.Role | nextcord.Member):
        message = TranslationsManager().get(self.__locale).gettext("Promoted {role_or_member} to DJ. Don’t scratch the vinyl !").format(
            role_or_member=role_or_member.mention
        )
        return nextcord.Embed(
            description=f":white_check_mark: {message}",
            colour=self.__configuration.colour
        )

    def dj_remove(self, role_or_member: nextcord.Role | nextcord.Member):
        message = TranslationsManager().get(self.__locale).gettext("{role_or_member} is off the decks for now.").format(
            role_or_member=role_or_member.mention
        )
        return nextcord.Embed(
            description=f":white_check_mark: {message}",
            colour=self.__configuration.colour
        )

    def forward(self):
        message = TranslationsManager().get(self.__locale).gettext("Who needs intros anyway ?")
        return nextcord.Embed(
            description=f":fast_forward: {message}",
            colour=self.__configuration.colour
        )

    def history(self, previous_tracks: List[QueuedTrack], page: int):
        embed = nextcord.Embed(
            title=TranslationsManager().get(self.__locale).gettext("History"),
            colour=self.__configuration.colour
        )
        self.__build_track_list(
            embed,
            previous_tracks,
            page,
            f"{TranslationsManager().get(self.__locale).gettext("Previous tracks")} :",
            TranslationsManager().get(self.__locale).gettext("Played")
        )
        return embed

    def join(self):
        message = TranslationsManager().get(self.__locale).gettext("Let's get this party started !")
        return nextcord.Embed(
            description=f":party_popper: {message}",
            colour=self.__configuration.colour
        )

    def jump(self, track: int):
        if track == 0:
            return self.next()
        message = TranslationsManager().get(self.__locale).gettext("Boom. Skipped straight to track {track}. Enjoy !").format(
            track=track + 1
        )
        return nextcord.Embed(
            description=f":track_next: {message}",
            colour=self.__configuration.colour
        )

    def leave(self):
        message = TranslationsManager().get(self.__locale).gettext("Mic dropped. I'm gone.")
        return nextcord.Embed(
            description=f":microphone: {message}",
            colour=self.__configuration.colour
        )

    def loop(self, mode: LoopMode):
        embed = nextcord.Embed(
            colour=self.__configuration.colour
        )
        if mode == LoopMode.OFF:
            message = TranslationsManager().get(self.__locale).gettext("Looping turned off. One play, no reruns.")
            embed.description = f":arrow_right: {message}"
        elif mode == LoopMode.TRACK:
            message = TranslationsManager().get(self.__locale).gettext("You must really love this one. Looping it on repeat.")
            embed.description = f":repeat_one: {message}"
        else:
            message = TranslationsManager().get(self.__locale).gettext("Get ready for the encore. And the encore's encore. Looping the queue !")
            embed.description = f":repeat: {message}"
        return embed

    def move(self, track: QueuedTrack, from_: int, to: int):
        message = TranslationsManager().get(self.__locale).gettext("Shifted {track_title} like a playlist ninja. Moved from {from_} to {to}.").format(
            track_title=bold(escape_markdown(track.title)),
            from_=from_ + 1,
            to=to + 1
        )
        return nextcord.Embed(
            description=f":ninja: {message}",
            colour=self.__configuration.colour
        )

    def next(self):
        message = TranslationsManager().get(self.__locale).gettext("Skipping the current track, I didn't like this one either.")
        return nextcord.Embed(
            description=f":track_next: {message}",
            colour=self.__configuration.colour
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

    def now(self, player_status: PlayerStatus):
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
            title=TranslationsManager().get(self.__locale).gettext("Now Playing"),
            description=(
                f"{bold(link(escape_link_text(truncate(player_status.queue.current_track.title, 50)), escape_link_url(player_status.queue.current_track.url)))}\n"
                f"{TranslationsManager().get(self.__locale).gettext("Queued by")} : {player_status.queue.current_track.member.mention}\n"
                f"\n"
                f"{status_icon} {bar_progress} {inline_code(f'[{elapsed_time}/{total_time}]')} {loop_icon} :sound: {round(player_status.audio_source.volume)}%"
            ),
            colour=self.__configuration.colour
        )
        embed.set_thumbnail(url=player_status.queue.current_track.thumbnail)
        embed.set_footer(
            text=f"{TranslationsManager().get(self.__locale).gettext("Source")} : {escape_markdown(player_status.queue.current_track.source)}"
        )
        return embed

    def pause(self):
        message = TranslationsManager().get(self.__locale).gettext("Playback paused. Take your time !")
        return nextcord.Embed(
            description=f":pause_button: {message}",
            colour=self.__configuration.colour
        )

    def play(self, tracks: List[QueuedTrack]):
        len_tracks = len(tracks)
        message = TranslationsManager().get(self.__locale).ngettext(
            "Added {track_title} to the queue ! This one’s gonna slap.",
            "Added {len_tracks} tracks to the queue ! Now that’s what I call a playlist.",
            len_tracks
        ).format(
            track_title=bold(escape_markdown(tracks[0].title)),
            len_tracks=bold(str(len_tracks))
        )
        embed = nextcord.Embed(
            description=f":cd: {message}",
            colour=self.__configuration.colour
        )
        return embed

    def previous(self):
        message = TranslationsManager().get(self.__locale).gettext("Because one listen wasn’t enough...")
        return nextcord.Embed(
            description=f":track_previous: {message}",
            colour=self.__configuration.colour
        )

    def __build_track_list(self, embed: nextcord.Embed, tracks: List[QueuedTrack], page: int, title: str, title2: str):
        len_tracks = len(tracks)
        if len_tracks == 0:
            max_pages = 1
        else:
            max_pages = math.ceil(len_tracks / 10)
        if page >= max_pages:
            raise EmbedException(
                "I can't show you page {page} out of {max_pages}.",
                page=page + 1,
                max_pages=max_pages
            )
        if len_tracks == 0:
            track_list = [
                italic(TranslationsManager().get(self.__locale).gettext("Nothing to show here"))
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
            value=TranslationsManager().get(self.__locale).ngettext(
                "{len_tracks} track",
                "{len_tracks} tracks",
                len_tracks
            ).format(
                len_tracks=len_tracks
            ),
            inline=True
        )
        embed.add_field(
            name=TranslationsManager().get(self.__locale).gettext("Page"),
            value=TranslationsManager().get(self.__locale).gettext("{page} our of {max_pages}").format(
                page=page + 1,
                max_pages=max_pages
            ),
            inline=True
        )

    def queue(self, player_status: PlayerStatus, page: int):
        embed = self.now(player_status)
        self.__build_track_list(
            embed,
            player_status.queue.next_tracks,
            page,
            TranslationsManager().get(self.__locale).gettext("Up next :"),
            TranslationsManager().get(self.__locale).gettext("In queue")
        )
        return embed

    def remove(self, track: QueuedTrack):
        message = TranslationsManager().get(self.__locale).gettext("Say goodbye to {track_title}. It didn’t make the cut.").format(
            track_title=bold(escape_markdown(track.title))
        )
        return nextcord.Embed(
            description=f":scissors: {message}",
            colour=self.__configuration.colour
        )

    def resume(self):
        message = TranslationsManager().get(self.__locale).gettext("Back in action ! Enjoy the tracks.")
        return nextcord.Embed(
            description=f":play_pause: {message}",
            colour=self.__configuration.colour
        )

    def rewind(self):
        message = TranslationsManager().get(self.__locale).gettext("That part was worth a second listen !")
        return nextcord.Embed(
            description=f":rewind: {message}",
            colour=self.__configuration.colour
        )

    def seek(self):
        message = TranslationsManager().get(self.__locale).gettext("Dropping the needle, classic move.")
        return nextcord.Embed(
            description=f":dart: {message}",
            colour=self.__configuration.colour
        )

    def __setting_repr(self, value: Any) -> str:
        if hasattr(value, "mention"):
            return value.mention
        if isinstance(value, bool):
            return inline_code(TranslationsManager().get(self.__locale).gettext(repr(value)))
        if isinstance(value, Enum):
            return inline_code(value.name)
        return inline_code(escape_markdown(repr(value)))

    def setting_set(self, name: str, value: Any):
        setting_name = TranslationsManager().get(self.__locale).gettext(name)
        setting_value = self.__setting_repr(value)
        message = TranslationsManager().get(self.__locale).gettext("All set ! {setting_name} is now {setting_value}.").format(
            setting_name=setting_name,
            setting_value=setting_value
        )
        return nextcord.Embed(
            description=f":tools: {message}",
            colour=self.__configuration.colour
        )

    def setting_reset(self, name: str, value: Any):
        setting_name = TranslationsManager().get(self.__locale).gettext(name)
        setting_value = self.__setting_repr(value)
        message = TranslationsManager().get(self.__locale).gettext("Boom ! {setting_name} is back to default: {setting_value}.").format(
            setting_name=setting_name,
            setting_value=setting_value
        )
        return nextcord.Embed(
            description=f":tools: {message}",
            colour=self.__configuration.colour
        )

    def shuffle(self):
        message = TranslationsManager().get(self.__locale).gettext("Shuffled the queue. I hope you like surprises !")
        return nextcord.Embed(
            description=f":twisted_rightwards_arrows: {message}",
            colour=self.__configuration.colour
        )

    def shutdown(self):
        message = TranslationsManager().get(self.__locale).gettext("Initiating shutdown sequence... it’s been an honor.")
        return nextcord.Embed(
            description=f":saluting_face: {message}",
            colour=self.__configuration.colour
        )

    def stop(self):
        message = TranslationsManager().get(self.__locale).gettext("Music stopped. The crowd goes silent.")
        return nextcord.Embed(
            description=f":stop_button: {message}",
            colour=self.__configuration.colour
        )

    def version(self, version: TonearmVersion):
        version_message = TranslationsManager().get(self.__locale).gettext("Version {version}, up and running !").format(
            version=inline_code(f"v{version.version}")
        )
        created_by_message = TranslationsManager().get(self.__locale).gettext("Crafted with :heart: by {authors}.").format(
            authors=", ".join(map(italic, version.authors))
        )
        return nextcord.Embed(
            description=(
                f":robot: {link('Tonearm', version.homepage)}\n"
                f"\n"
                f"{version_message}\n"
                f"{created_by_message}"
            ),
            colour=self.__configuration.colour,
        )

    def volume(self, volume: int):
        message = TranslationsManager().get(self.__locale).gettext("Volume’s now {volume}%. Don’t blame me if it’s too loud !").format(
            volume=volume
        )
        return nextcord.Embed(
            description=f":sound: {message}",
            colour=self.__configuration.colour
        )

    def votenext(self, status: VoteStatus):
        if status.needed_votes > 0:
            emote = ":ballot_box:"
            message = TranslationsManager().get(self.__locale).ngettext(
                "We need {needed_votes} more vote to skip this track.",
                "We need {needed_votes} more votes to skip this track.",
                status.needed_votes
            ).format(
                needed_votes=status.needed_votes,
            )
        else:
            emote = ":track_next:"
            message = TranslationsManager().get(self.__locale).gettext("Track skipped by popular demand !")
        return nextcord.Embed(
            description=f"{emote} {message}",
            colour=self.__configuration.colour
        )