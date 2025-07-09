import re
import argparse

import nextcord


__COLOR_REGEX = re.compile(r"(?i)^#([a-f0-9]{6})$")

def color(colour: str) -> nextcord.Colour:
    match = __COLOR_REGEX.match(colour)
    if not match:
        raise argparse.ArgumentTypeError(f"{colour} is not a valid color")
    return nextcord.Colour(int(f"0x{match.group(1).upper()}", 16))