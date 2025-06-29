from bin.text_manipulation import *
from bin.data_access import file_read

COPYRIGHT = f"{bold('LPRT')} {italic(file_read('version.txt'))} - (c) Justus Decker 2024 - 2025"

SUBS = {
    'main': ['Main'],
    'automations': ['Main','Automations'],
    'options': ['Main','Options'],
    'tg': ['Main' , 'Automation' , 'Thumbnail Generator']
}

def header(key_sub: str,subs: list[str]= []) -> str:
    return f"""
{COPYRIGHT}

{bold(" > ").join(SUBS[key_sub]+subs)}

Select your option:
"""


MENU_MESSAGE = f"""
{header('main')}
(1) Record
(2) Automation
(3) {color816(strikethrough('Deploy'),31)}
(4) Create Lets Play File
(5) Options
(0) Exit
"""

MENU_AUTOMATION_MESSAGE = f"""
{header('automations')}
(1) Thumbnail Generate
(2) {color816(strikethrough('Fetch Audio'),31)}
(3) {color816(strikethrough('Fix Audio'),31)}
(4) {color816(strikethrough('Render'),31)}
(0) Back
"""

MENU_OPTIONS_MESSAGE = f"""
{header('options')}
(1) Create {bold('options.json')} - OBS
(2) Set current lets play id
(3) Create {bold('default_tad.json')}
(4) Create {bold('lets_plays.csv')}
(0) Back
"""

def thumbnail_automation_sub_menu(sub:str) -> str:
    return f"""
{COPYRIGHT}    
    
{bold(f'Main > Automation > Thumbnail Generator > Select LP')}

Select your Option:
    """

USER_INPUT_NUM_UNMATCHED = color816(bold('This option does not exist'),31)

DEFAULT_THUMBNAIL_SIZE = (1280,720)

DEFAULT_OBS_SETTINGS = {
    "ip": "",
    "port": 1234,
    "pw": "",
    "timeout": 1
}

DEFAULT_TAD = [
    {
        "pos": [0,0]
    },
    {
        "path": "test_logo.png",
        "scale": 1,
        "rot": 0,
        "pos": [0,0]
    },
    {
        "path": "",
        "scale": 1,
        "rot": 0,
        "color": [255,255,255,255],
        "ol_color": [1,1,1,255],
        "size": 40,
        "pos": [0,0]
    }
]