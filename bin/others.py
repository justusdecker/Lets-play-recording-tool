__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.3.112"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"
from os import getcwd
from bin.text_manipulation import err, bold
from bin.constants import COPYRIGHT, header,ERROR_003
from bin.constants import (
    feedback,
    FB_SUCCESS,
    FB_WARNING,
    FB_ERROR,
    FB_INFO,
    FB_ENTER
)

def binpi(text : str, inp: str = '') -> int:
    """
    b: better
    inp: input
    i: int
    """
    
    user_input = ''
    while not user_input.isdecimal():
        print(text, end='')
        user_input = input(f'{inp}\033[92m\033[3m')
        feedback(FB_ENTER)
        print('\033[23m\033[39m',end='')
    return int(user_input)

def binps(text : str, inp: str = '') -> int:
    """
    b: better
    inp: input
    i: int
    """
    
    user_input = ''
    while not user_input:
        print(text, end='')
        user_input = input(f'{inp}\033[92m\033[3m')
        feedback(FB_ENTER)
        print('\033[23m\033[39m',end='')
    return user_input

def input_in_range(start,end,text):
    inp = binpi(text)

    if inp >= start and inp <= end:
        return inp
    else:
        feedback(FB_ERROR)
        err('Outside range')

def input_episode_range(max_eps:list[int], lp_names: list[str]) -> None | tuple[int, tuple[int, int]]:
    
    if len(max_eps) != len(lp_names):
        feedback(FB_ERROR)
        err('ValueError')
        return
    # SET LP
    listed_lets_plays = "\n".join([f"({idx}) {lp}" for idx, lp in enumerate(lp_names)])
    
    lp_id = binpi(f"{header('tg',['Set Lets Play'])}{listed_lets_plays}\n")
    
    if lp_id >= len(lp_names):
        feedback(FB_ERROR)
        err('Input out of range')
        return
    
    
    # SET MODE
    MODE_SET = f"""
{header('tg',['Set MODE'])}
(1) all
(2) in range
(3) one
    """
    RANGE_START = header('tg',['Set RANGE START']) + f'0 - {max_eps[lp_id]-1}\n'
    RANGE_END = header('tg',['Set RANGE END']) + f'0 - {max_eps[lp_id]-1}\n'
    RANGE_ONE = header('tg',['Set Index']) + f'0 - {max_eps[lp_id]-1}\n'
    match binpi(MODE_SET):
        case 1:
            ep_range = (0,max_eps[lp_id])
        case 2:
            _start = binpi(RANGE_START)
            if _start >= max_eps[lp_id]:
                feedback(FB_ERROR)
                err('Input out of range')
                return
            _end = binpi(RANGE_END + f'\n{_start} - {max_eps[lp_id]-1}\n')
            if _end >= max_eps[lp_id]:
                feedback(FB_ERROR)
                err('Input out of range')
                return
            if _start > _end:
                feedback(FB_ERROR)
                err('Input out of range')
                return
            ep_range = (_start, _end+1)
        case 3:
            _index = binpi(RANGE_ONE)
            ep_range = (_index,_index)
        case _:
            feedback(FB_ERROR)
            err(ERROR_003)
            return None
    return lp_id, ep_range

def convert_to_tc(t:float):
    h, m, s = t // 60 // 60,t // 60, t % 60
    h, m, s = int(h), int(m), int(s)
    h = f'0{h}' if h < 10 else str(h)
    m = f'0{m}' if m < 10 else str(m)
    s = f'0{s}' if s < 10 else str(s)
    return f'{h}:{m}:{s}'

import winotify
from winotify import audio

"""
Documentation: https://pypi.org/project/winotify/
"""

TOAST = winotify.Notification('LPRT','Welcome','Up & Running',f'{getcwd()}\\logo.ico')
TOAST.set_audio(audio.Mail,False)

def toast_finished(msg: str=""):
    TOAST.title = 'Job finished'
    TOAST.msg = msg
    TOAST.show()
