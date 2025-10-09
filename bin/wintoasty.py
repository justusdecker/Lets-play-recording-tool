from bin.welcome_popup import WELCOME
from bin.translation import gtran
WELCOME.update_message(f'{gtran("bin::welcome::load")} {__name__}')


from winotify import Notification, audio
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