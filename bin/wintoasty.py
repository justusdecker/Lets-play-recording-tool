from winotify import Notification, audio
from os import getcwd

"""
Documentation: https://pypi.org/project/winotify/
"""

TOAST = Notification('LPRT','Welcome','Up & Running',f'{getcwd()}\\logo.ico')
TOAST.set_audio(audio.Mail,False)

def toast_finished(msg: str=""):
    TOAST.title = 'Job finished'
    TOAST.msg = msg
    TOAST.show()