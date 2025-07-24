__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.10.114"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"


from bin.version import VERSION

COPYRIGHT = f"LPRT {VERSION} - (c) Justus Decker 2024 - 2025"

DISCLAIMER = f"""
{COPYRIGHT}
Welcome to LPRT

This Tool is currently Work in Progress!
Some features might not work as expected & can cause data loss! Be careful!
"""

DEFAULT_THUMBNAIL_SIZE = (1280,720)

LP_KEYS = [
    'version',
    'episode_path',
    'tad_path',
    'name',
    'game_name',
    'episode_length',
    'description_path'] 

EP_KEYS = [
    'video_path',
    'audio_mic_path',
    'audio_desktop_path',
    'thumbnail_path',
    'thumbnail_frame',
    'has_problem',
    'audio_mic_edit1_path',
    'audio_mic_edit2_path',
    'audio_desktop_edit1_path',
    'audio_desktop_edit2_path',
    'title',
    'episode_number',
    'upload_at',
    'final_audio'
]

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
OBS_SETTINGS_PATH = f'{ROOT}obs_settings.json'
    
#! ERRORS
ewf = 'Exit current workflow.'
exp = 'Exiting App!'
ERROR_001 = f'[E001] User input is not in range. {ewf}'
ERROR_002 = f'[E002] file already exists. {ewf}'
ERROR_003 = f'[E003] This option does not exist. {ewf}'
ERROR_004 = f'[E004] No connection to OBS! {ewf}'
ERROR_005 = f'[E005] Keyboard interrupt! {ewf}'
ERROR_006 = f'[E006] Destination not set. {ewf}'
ERROR_007 = f'[E007] file does not exist. {ewf}'
ERROR_008 = f'[E008] ModuleLoadFailure. {exp}'
ERROR_009 = f"[E009] Something went wrong. No TAD found. {ewf}"
ERROR_010 = f'[E010] FFMPEG is not installed. {exp}'
ERROR_011 = f'[E011] FFPLAY is not installed. {exp}'
ERROR_012 = f'[E012] FFPROBE is not installed. {exp}'