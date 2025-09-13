from bin.translation import gtran
from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

try: #Fix for issue: #125
    from winotify import Notification, audio
except:
    from tkinter.messagebox import showerror
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nwinotify')
    quit()
from os import getcwd

TOAST = Notification('LPRT','Welcome','Up & Running',f'{getcwd()}\\bin\\data\\img\\logo.ico')
TOAST.set_audio(audio.Mail,False)

def toast_finished(msg: str=""):
    """
    Displays a Windows toast notification indicating that a job has finished.

    This function reuses a pre-configured global `TOAST` Notification object,
    updates its title and message, and then displays it.
    
    Documentation: https://pypi.org/project/winotify/
    """
    TOAST.title = gtran("bin::wintoasty::toast_finished_msg")
    TOAST.msg = msg
    TOAST.show()