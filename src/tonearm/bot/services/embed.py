from typing import List

import nextcord
from injector import singleton

from tonearm.bot.data import TrackMetadata


@singleton
class EmbedService:

    @staticmethod
    def error(e):
        return nextcord.Embed(
            description=f":x: {str(e)}",
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
    def play(tracks: List[TrackMetadata]):
        embed = nextcord.Embed(
                colour=nextcord.Colour.dark_purple()
            )
        if len(tracks) > 1:
            embed.description = f":cd: Added **{len(tracks)} tracks** to the queue! Now that’s what I call a playlist."
        else:
            embed.description = f":cd: Added **{tracks[0].title}** to the queue ! This one’s gonna slap."
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