from bin.text_manipulation import *
from bin.data_access import file_read

COPYRIGHT = f"{bold('LPRT')} {italic(file_read('version.txt'))} - (c) Justus Decker 2024 - 2025"

MENU_MESSAGE = f"""
{COPYRIGHT}

{bold('Main >')}

Select your option:
(1) Record - {color816(bold('ALPHA'),35)}
(2) Automation - {color816(bold('ALPHA'),35)}
(3) {color816(strikethrough('Deploy'),31)}
(4) Data
(5) Options
(0) Exit
"""

MENU_AUTOMATION_MESSAGE = f"""
{COPYRIGHT}

{bold('Main > Automations >')}

Select your option:
(1) Thumbnail Generate
(2) {color816(strikethrough('Fetch Audio'),31)}
(3) {color816(strikethrough('Fix Audio'),31)}
(4) {color816(strikethrough('Render'),31)}
(5) Back
"""

MENU_DATA_MESSAGE = f"""
{COPYRIGHT}

{bold('Main > Data')}

Select your option:
(1) {color816(strikethrough('Create a new file'),31)}
(2) Create a new entry - {color816(bold('ALPHA'),35)}
(3) {color816(strikethrough('Update'),31)}
(4) {color816(strikethrough('Read'),31)}
(5) {color816(strikethrough('Delete'),fg=31)}
(0) Exit
"""
def data_sub_menu(sub: str) -> str:
    return f"""
{COPYRIGHT}

{bold(f'Main > Data > {sub}')}

Select your option:
(1) Lets Play
(2) Episode
(3) Thumbnail Automation Data
(0) Exit
"""

def thumbnail_automation_sub_menu(sub:str) -> str:
    return f"""
{COPYRIGHT}    
    
{bold(f'Main > Automation > Thumbnail Generator > Select LP')}

Select your Option:
    """

USER_INPUT_NUM_UNMATCHED = color816(bold('This option does not exist'),31)

DEFAULT_THUMBNAIL_SIZE = (1280,720)