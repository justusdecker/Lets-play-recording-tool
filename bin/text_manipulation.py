def strikethrough(text: str) -> str:
    """ set strikethrough mode by using escape sequences """
    return f"\033[9m{text}\033[9m"
def color816(text: str, color: int) -> str:
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
    return f"\033[9m{text}\033[9m"