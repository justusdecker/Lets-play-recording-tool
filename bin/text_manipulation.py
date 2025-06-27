COLOR_TABLE816FG = [90 + i for i in range(8)]  + [30 + i for i in range(10)]
COLOR_TABLE816BG = [40 + i for i in range(10)] + [100 + i for i in range(8)]

def err(text: str) -> str:
    return color816(text,31)

def strikethrough(text: str) -> str:
    """ set strikethrough mode by using escape sequences """
    return f"\033[9m{text}\033[29m"

def color816(text: str, fg: int, bg: int= 40) -> str:
    """ 
    set text color by using escape sequences.
    
    **8 - 16 Colors**
    
    Color Table
    ---
    
    |Color|FG CC|BG CC|
    |---|---|---|
    |Black|30|40|
    |Red|31|41|
    |Green|32|42|
    |Yellow|33|43|
    |Blue|34|44|
    |Magenta|35|45|
    |Cyan|36|46|
    |White|37|47|
    |Default|39|49|
    |Bright Black|90|100|
    |Bright Red|91|101|
    |Bright Green|92|102|
    |Bright Yellow|93|103|
    |Bright Blue|94|104|
    |Bright Magenta|95|105|
    |Bright Cyan|96|106|
    |Bright White|97|107|
    """
    
    if fg not in COLOR_TABLE816FG or bg not in COLOR_TABLE816BG:
        raise Exception('Unknown Color')
    
    return f"\033[{fg}m\033[{bg}m{text}\033[39m\033[49m"

def italic(text: str) -> str:
    """ set italic mode by using escape sequences """
    return f"\033[3m{text}\033[23m"

def bold(text: str) -> str:
    """ set bold mode by using escape sequences """
    return f"\033[1m{text}\033[22m"

def underline(text: str) -> str:
    """ set underline mode by using escape sequences """
    return f"\033[4m{text}\033[24m"

def inverse_color(text: str) -> str:
    """ set inverse color by using escape sequences """
    return f"\033[7m{text}\033[27m"

def hidden(text: str) -> str:
    """ set hidden by using escape sequences """
    return f"\033[8m{text}\033[28m"