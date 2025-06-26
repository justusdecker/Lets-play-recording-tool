def strikethrough(text: str) -> str:
    """ set strikethrough mode by using escape sequences """
    return f"\033[9m{text}\033[9m"