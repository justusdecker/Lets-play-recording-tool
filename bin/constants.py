__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.10.114"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from bin.data_access import cnef, json_write, csv_write, isfile
from bin.version import VERSION

COPYRIGHT = f"LPRT {VERSION} - (c) Justus Decker 2024 - 2025"

DEFAULT_THUMBNAIL_SIZE = (1280,720)

DEFAULT_OBS_SETTINGS = {
    "ip": "",
    "port": 1234,
    "pw": "",
    "timeout": 1
}

DEFAULT_TAD = [
    {
        "pos": [0,0],
        "r_pos": [[0,0],[0,0]],
        "r_scale": [0,0],
        "r_rot": [0,0],
        "center": True,
        "scale": 1.35,
        "rot": 0
    },
    {
        "path": "test_logo.png",
        "scale": 1,
        "rot": 0,
        "pos": [0,0],
        "center": True
    },
    {
        "path": "",
        "scale": 1,
        "rot": 0,
        "color": [255,255,255,255],
        "ol_color": [1,1,1,255],
        "size": 40,
        "pos": [0,0],
        "center": True
    }
]

#! PATHS

from os import getlogin
from os.path import isfile
USERNAME = getlogin()
del getlogin

ROOT = f'C:\\Users\\{USERNAME}\\lprt\\'

AUDIO_FOLDER = f'{ROOT}audio\\'
VIDEO_FOLDER = f'{ROOT}video\\'
TAD_FOLDER = f'{ROOT}tad\\'
TEMP_FOLDER = f'{ROOT}temp\\'
THUMBNAIL_FOLDER = f'{ROOT}thumbnails\\'
FIXED_AUDIO_FOLDER = f'{ROOT}audio_fixed\\'

LETS_PLAY_FILE_PATH = f'{ROOT}lets_plays.csv'

cnef(AUDIO_FOLDER)
cnef(FIXED_AUDIO_FOLDER)
cnef(THUMBNAIL_FOLDER)
cnef(VIDEO_FOLDER)
cnef(TAD_FOLDER)
cnef(TEMP_FOLDER)

if not isfile('obs_settings.json'):
    json_write('obs_settings.json',DEFAULT_OBS_SETTINGS)
if not isfile(LETS_PLAY_FILE_PATH):
    csv_write(LETS_PLAY_FILE_PATH)
    
#! ERRORS
ewf = 'Exit current workflow.'
ERROR_001 = f'[E001] User input is not in range. {ewf}'
ERROR_002 = f'[E002] file already exists. {ewf}'
ERROR_003 = f'[E003] This option does not exist. {ewf}'
ERROR_004 = f'[E004] No connection to OBS! {ewf}'
ERROR_005 = f'[E005] Keyboard interrupt! {ewf}'
ERROR_006 = f'[E006] Destination not set. {ewf}'
ERROR_007 = f'[E007] file does not exist. {ewf}'