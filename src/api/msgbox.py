"""
A Wrapper for the win32ui.MessageBox

More information: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox
"""

from win32ui import MessageBox
from win32con import MB_ICONASTERISK, MB_ICONEXCLAMATION, MB_ICONHAND, MB_OK
from win32api import MessageBeep

class SoundFlags:
    INFORMATION = MB_ICONASTERISK
    WARNING = MB_ICONEXCLAMATION
    ERROR = MB_ICONHAND
    OK = MB_OK

class ReturnFlags:
    OK = 1
    CANCEL = 2
    ABORT = 3
    RETRY = 4
    IGNORE = 5
    YES = 6
    NO = 7
    TRY_AGAIN = 10
    CONTINUE = 11

class Buttons:
    ABORT_RETRY_IGNORE = 0x00000002
    CANCEL_RETRY_CONTINUE = 0x00000006
    HELP = 0x00004000
    OK = 0x00000000
    OK_CANCEL = 0x00000001
    RETRY_CANCEL = 0x00000005
    YES_NO = 0x00000004
    YES_NO_CANCEL = 0x00000003

class Icons:
    WARNING = 0x00000030
    INFORMATION = 0x00000040
    QUESTION = 0x00000020
    ERROR = 0x00000010
    
class DefaultButton:
    BTN1 = 0x00000000
    BTN2 = 0x00000100
    BTN3 = 0x00000200
    BTN4 = 0x00000300

class Modals:
    APPL = 0x00000000
    SYSTEM = 0x00001000
    TASK = 0x00002000

class WindowOptions:
    DEFAULT_DESKTOP_ONLY = 0x00020000
    RIGHT = 0x00080000
    RT_LEADING = 0x00100000
    SET_FOREGROUND = 0x00010000
    TOPMOST = 0x00040000
    SERVICE_NOTIFICATION = 0x00200000
    
class MSGBoxPresets:
    CRITICAL_RETRY = Icons.ERROR | Buttons.ABORT_RETRY_IGNORE | DefaultButton.BTN2
    CONFIRM_QUESTION = Icons.QUESTION | Buttons.YES_NO | WindowOptions.SET_FOREGROUND
    SYSTEM_ALERT = Icons.WARNING | Buttons.OK | Modals.SYSTEM | WindowOptions.TOPMOST
    SAFE_INFO = Icons.INFORMATION | Buttons.OK_CANCEL | DefaultButton.BTN2
    
def msgbox(title: str, msg: str, style: int = MSGBoxPresets.SAFE_INFO, snd: int = SoundFlags.OK):
    MessageBeep(snd)
    return MessageBox(msg, title, style)


# - Test -
msgbox('Info - LPRT', 'The cake is a lie...')