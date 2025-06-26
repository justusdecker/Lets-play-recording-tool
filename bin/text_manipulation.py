def strikethrough(text: str) -> str:
    """ set strikethrough mode by using escape sequences """
    return f"\033[9m{text}\033[9m"
def tcolor(text: str, color: int) -> str:
    """ 
    set text color by using escape sequences.
    
    |Color|FG CC|BG CC|
    |---|---|---|
    |Black|30|40|
    Red	31	41
    Green	32	42
    Yellow	33	43
    Blue	34	44
    Magenta	35	45
    Cyan	36	46
    White	37	47
    Default	39	49
    
    """
    return f"\033[9m{text}\033[9m"