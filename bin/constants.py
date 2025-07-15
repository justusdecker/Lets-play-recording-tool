__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.8.5"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from win32api import Beep

FB_ENTER = (600,100,1)
FB_BACK = (400,100,1)
FB_ERROR = (500,100,3)
FB_WARNING = (500,100,2)
FB_CRITICAL = (500,400,10)
FB_SUCCESS = (750,100,1)
FB_INFO = (700,100,1)
def feedback(key: str) -> None:
    """
    Gives user sound feedback
    """
    f,d,i = key
    for it in range(i):
        Beep(f,d)

from bin.text_manipulation import *

from bin.version import VERSION

COPYRIGHT = f"{bold('LPRT')} {italic(VERSION)} - (c) Justus Decker 2024 - 2025"

SUBS = { 'main': ['Main'],'automations': ['Main','Automations'],'options': ['Main','Options'], 'tg':['Main', 'Automations', 'Thumbnail']}

MENU_OPTIONS = ['Record', 'Automation', color816(strikethrough('Deploy'),31), 'Options'] # main

MENU_AUTOMATION_OPTIONS = ['Thumbnail Generate', 'Fetch Audio', 'Fix Audio', 'Send to Audacity', 'Compare Audio & render'] # automations

MENU_SETTINGS_OPTIONS = [f"Create {bold('options.json')} - OBS", 'Set current lets play id', f"Create {bold('default_tad.json')}", f"Create {bold('lets_plays.csv')}"] # options

def header(key_sub: str,subs: list[str]) -> str:
    tmp = bold(" > ").join(SUBS[key_sub]+subs) + ' >'
    return f'{COPYRIGHT}\n\n{tmp}\n\nSelect your option:\n'

def menu(options: list[str], key: str, subs: list[str] = [], exit_name: str = 'Exit'):
    """
    Returns the menu
    """
    _ret = header(key,subs) + '\n'
    
    for index, option in enumerate(options):
        _ret += f'({index + 1}) {option}\n'
    _ret += f'(0) {exit_name}\n'
    return _ret

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
        "pos": [0,0],
        "r_pos": [[0,0],[0,0]],
        "r_scale": [1,1],
        "r_rot": [0,0],
        "center": True
    }
]

"""
AAA
OLD
[
    {
        "pos": [0,0],
        "r_pos": [[0,0],[0,0]],
        "r_scale": [-0.05,0.05],
        "r_rot": [-8,8],
        "center": true,
        "scale": 1.35,
        "rot": 0
    },
    {
        "path": "E:\\scheduleone.png",
        "scale": 0.2,
        "rot": 0,
        "pos": [650,200],
        "center": true
    },
    {
        "path": "",
        "scale": 1,
        "rot": 0,
        "color": [234,232,184,255],
        "ol_color": [57,72,45,255],
        "size": 120,
        "pos": [550,450],
        "center": true
    }
]
"""


#! PATHS

from os import getlogin
USERNAME = getlogin()
del getlogin

ROOT = f'C:\\Users\\{USERNAME}\\jri_data\\'

AUDIO_FOLDER = f'{ROOT}audio\\'
VIDEO_FOLDER = f'{ROOT}video\\'
TEMP_FOLDER = f'{ROOT}temp\\'
THUMBNAIL_FOLDER = f'{ROOT}thumbnails\\'
FIXED_AUDIO_FOLDER = f'{ROOT}audio_fixed\\'

#! ERRORS
ewf = 'Exit current workflow.'
ERROR_001 = f'[E001] User input is not in range. {ewf}'
ERROR_002 = f'[E002] file already exists. {ewf}'
ERROR_003 = f'[E003] This option does not exist. {ewf}'
ERROR_004 = f'[E004] No connection to OBS! {ewf}'
ERROR_005 = f'[E005] Keyboard interrupt! {ewf}'
ERROR_006 = f'[E006] Destination not set. {ewf}'
ERROR_007 = f'[E007] file does not exist. {ewf}'


from subprocess import run, CREATE_NO_WINDOW

## FFMPEG COMMANDS
# View documentation > FFMPEG

FFMPEG_DEFAULT = ['ffmpeg', '-v', 'quiet', '-stats' , '-loglevel', 'error', '-y']

FFMPEG_CONVERT_AUDIO_TYPE = [*FFMPEG_DEFAULT, '-i', '__IN__', '__OUT__']

FFMPEG_EXTRACT = [*FFMPEG_DEFAULT, '-i', '__IN__', '-map', '0:a:0', '-c:a', 'copy', '__OUT1__', '-map', '0:a:1', '-c:a', 'copy','__OUT2__']

FFMPEG_OPTIMIZED_EXTRACT = [*FFMPEG_DEFAULT, '-i', '__IN__', '-map', '0:a:0', '-c:a', 'copy', '__OUT1__', '-map',  '0:a:1', '-c:a', 'copy', '__OUT2__']

FFMPEG_AUDIO_COMBINE = [*FFMPEG_DEFAULT, '-i', "__IN1__", '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"]

FFMPEG_AUDIO_COMBINE_TRUNCATED = [*FFMPEG_DEFAULT, '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN1__", '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"] # '-ac', '2', amerge=inputs=2

FFMPEG_AUDIO_PF_LN_L = [*FFMPEG_DEFAULT, '-i', '__IN__', '-af','highpass=f=175, lowpass=f=13000, loudnorm=-15, compand=0|0:1|1:0/-3|10/-3|20/-3:0.1:0:0:0', '__OUT__']

FFMPEG_VIDEO_RENDER = [*FFMPEG_DEFAULT, '-an', '-i', '__VIDEO__', '-i', '__AUDIO__', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '__OUTPUT__']

FFMPEG_GET_FRAME = [*FFMPEG_DEFAULT, '-ss', '__TIME__', '-i', '__IN__', '-frames:v', '1', 'temp.png']

FFMPEG_GET_LENGTH = ['ffprobe', '-v', 'error', '-select_streams', 'stream=duration', '-of', 'default=noprint_warpper=1:nokey=1', '__IN__']


#- Currently total broken. Will be worked later on
#SOX_CREATE_NOISE_PROFILE = ['sox', '__IN__', '-n', 'noiseprof', '__OUT__']
#SOX_APPLY_NR = ['sox', '__IN__', '__OUT__', 'noisered', '__PROF__', '0.1']
#FFMPEG_GET_SILENCE = ['ffmpeg', '-i',  '__IN__', '-af', 'silencedetect=n=__SIL__dB:d=__DUR__' ,'-f', 'null', '2>data.txt']
#FFMPEG_EXPORT_SILENCE = ['ffmpeg','-y', '-ss', '__SS__', '-t', '__TO__', '-i', '__IN__', '__OUT__']
#FFMPEG_CUT = [*FFMPEG_DEFAULT, '-ss' ,'__START__', '-to', '__END__', '-i', "__IN__", '-c', 'copy', "__OUT__"] # '-ac', '2', amerge=inputs=2

def ffmpeg_build(cmd: list[str], replacer: dict[str,str]):
    """
    This function takes the FFMPEG command and replaces all of the keys that can be found in the command!
    
    If you forget to change a key, this will result in an error from FFMPEG. No Exception raises.
    
    Is a key not existent it will replace nothing.
    """
    for key in replacer:
        cmd = [arg.replace(key,str(replacer[key])) if key in arg else arg for arg in cmd]
    return cmd

def ffmpeg_run(cmd: list[list], replacer: dict[str,str]):
    """
    This function runs your FFMPEG command. Before this happens this function calls ffmpeg_build to replace some essential variables.
    
    Subprocess is used to call FFMPEG
    
    The settings are: NO WINDOW <- Don't work with terminal applications!
    
    shell= True is compatible with limiter compand
    """
    run(ffmpeg_build(cmd,replacer), CREATE_NO_WINDOW,)
    #return run(ffmpeg_build(cmd,replacer), CREATE_NO_WINDOW, capture_output=True, text=True)