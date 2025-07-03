__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__license__ = "CC BY-NC-ND"
__version__ = "0.3.115"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from bin.text_manipulation import *
from bin.data_access import file_read
from bin.version import VERSION

COPYRIGHT = f"{bold('LPRT')} {italic(VERSION)} - (c) Justus Decker 2024 - 2025"

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
(4) Options
(0) Exit
"""

MENU_AUTOMATION_MESSAGE = f"""
{header('automations')}
(1) Thumbnail Generate
(2) Fetch Audio
(3) 'Fix Audio
(4) Render
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


#! PATHS

from os import getlogin
USERNAME = getlogin()
del getlogin

ROOT = f'C:\\Users\\{USERNAME}\\jri_data\\'

AUDIO_FOLDER = f'{ROOT}audio\\'
THUMBNAIL_FOLDER = f'{ROOT}thumbnails\\'
FIXED_AUDIO_FOLDER = f'{ROOT}{AUDIO_FOLDER}audio_fixed\\'

#! ERRORS
ewf = 'Exit current workflow.'
ERROR_001 = f'[E001] User input is not in range. {ewf}'
ERROR_002 = f'[E002] file already exists. {ewf}'
ERROR_003 = f'[E003] This option does not exist. {ewf}'
ERROR_004 = f'[E004] No connection to OBS! {ewf}'
ERROR_005 = f'[E005] Keyboard interrupt! {ewf}'
ERROR_006 = f'[E006] Destination not set. {ewf}'
ERROR_007 = f'[E007] file does not exist. {ewf}'