from nextcord.utils import escape_markdown

def escape_link_text(text: str) -> str:
    return text.replace('[', '［').replace(']', '］')

def escape_link_url(url: str) -> str:
    return url.replace('<', '\\<').replace('>', '\\>')

def link(text: str, url: str) -> str:
    return f"[{text}](<{url}>)"

def bold(text: str) -> str:
    return f"**{text.replace('**', '\\*\\*')}**"

def inline_code(text: str) -> str:
    return f"`{text.replace('`', '\\`')}`"