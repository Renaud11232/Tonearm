def truncate(string: str, max_length: int) -> str:
    return f"{string[:max_length]}{'...' if len(string) > max_length else ''}"