__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__license__ = "CC BY-NC-ND"
__version__ = "0.3.115"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from bin.text_manipulation import *

from bin.version import VERSION

COPYRIGHT = f"{bold('LPRT')} {italic(VERSION)} - (c) Justus Decker 2024 - 2025"

SUBS = { 'main': ['Main'],'automations': ['Main','Automations'],'options': ['Main','Options']}

MENU_OPTIONS = ['Record', 'Automation', color816(strikethrough('Deploy'),31), 'Options'] # main

MENU_AUTOMATION_OPTIONS = ['Thumbnail Generate', 'Fetch Audio', 'Fix Audio', 'Compare Audio & render'] # automations

MENU_SETTINGS_OPTIONS = [f"Create {bold('options.json')} - OBS", 'Set current lets play id', f"Create {bold('default_tad.json')}", f"Create {bold('lets_plays.csv')}"] # options

def header(key_sub: str,subs: list[str]) -> str:
    tmp = bold(" > ").join(SUBS[key_sub]+subs) + ' >'
    return f'{COPYRIGHT}\n\n{tmp}\n\nSelect your option:'

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

# Simply change the ending of a file to convert it. So .mp3 -> .wav
#? Need an input path & output path
FFMPEG_CONVERT_AUDIO_TYPE = ['ffmpeg', '-n', '-i', '__IN__', '__OUT__']

# A simple way to get rid of some unnesseccary frequencys & some noises.
# Works in most cases with default settings.
#! Must be enhanced in the future
#? Need an input path & output path

limiter = 'compand=0|0:1|1:0/-3|10/-3|20/-3:0.1:0:0:0'
FFMPEG_LIMITER = ['ffmpeg', '-y', '-i', '__IN__', '-af', limiter, '__OUT__']

# Normalizes audio to -15 decibel
#? Need an input path & output path
FFMPEG_LOUDNESS_NORMALIZATION = ['ffmpeg', '-y', '-i', '__IN__', '-af', 'loudnorm=-15', '__OUT__']

# Extract audio from a video file
#! Will be optimized in the futere by splitting the output to two output streams
#? Need an input path, output path & a mapping id <- this is the track you want(starts by 1)
FFMPEG_EXTRACT = ['ffmpeg', '-y', '-i', '__IN__', '-map', '0:__MAPPING__', '__OUT__']

FFMPEG_OPTIMIZED_EXTRACT = ['ffmpeg', '-y', '-i', '__IN__', '-map', '0:1', '__OUT1__', '-map', '0:2', '__OUT2__']

# Combine two audio tracks
#? Need an input path & output path
FFMPEG_AUDIO_COMBINE = ['ffmpeg', '-y', '-i', "__IN1__", '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"]# '-ac', '2', amerge=inputs=2

# Combine two audio tracks
#? Need an input path & output path
FFMPEG_AUDIO_COMBINE_TRUNCATED = ['ffmpeg', '-y', '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN1__", '-ss' ,'00:00:00', '-to', '00:02:00', '-i', "__IN2__", '-filter_complex', '[0:0]volume=__VOLUME1__[a];[1:0]volume=__VOLUME2__[b];[a][b]amix=inputs=2:duration=longest', "__OUT__"] # '-ac', '2', amerge=inputs=2

FFMPEG_VIDEO_RENDER = ['ffmpeg', '-y', '-an', '-i', '__VIDEO__', '-i', '__AUDIO__', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '__OUTPUT__']

#!A quick non pro explanation about the map argument
#
#? when you split the argument by ':' you get two values:
#
#. the first one is the file identifier ( so if have two files input you can map 0:? and 1:? to the output)
#. the second is the stream identifier:
#+      here you can use:
#+          a       audio stream
#+          v       video stream
#+          0-1234  the stream you want(audio and video i guess?)


def ffmpeg_build(cmd: list[str], replacer: dict[str,str]):
    """
    This function takes the FFMPEG command and replaces all of the keys that can be found in the command!
    
    If you forget to change a key, this will result in an error from FFMPEG. No Exception raises.
    
    Is a key not existent it will replace nothing.
    """
    for key in replacer:
        cmd = [arg.replace(key,replacer[key]) if key in arg else arg for arg in cmd]
    deb(cmd)
    return cmd

def ffmpeg_run(cmd: list[list], replacer: dict[str,str]):
    """
    This function runs your FFMPEG command. Before this happens this function calls ffmpeg_build to replace some essential variables.
    
    Subprocess is used to call FFMPEG
    
    The settings are: NO WINDOW <- Don't work with terminal applications!
    
    shell= True is compatible with limiter compand
    """
    
    run(ffmpeg_build(cmd,replacer), CREATE_NO_WINDOW)