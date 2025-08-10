from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

"""
This Module contains everything you need to connect to the Audacity in a safe way.

Contains:
- Sending Commands
- Receiving Results from Audacity
- Errorhandling

How to enable the Audacity pipeline?
Open Audacity
Go to: Edit > Settings > Module > enable mod-script-pipe
Reopen Audacity & Reopen LPRT(When open)
"""
import win32file
from io import TextIOWrapper
class AudacityPipelineError(Exception):
    pass

class AudacityFileAccess:
    """
    A Dataclass to easy access the Audacity mod-pipe
    
    Includes:
        - TO_NAME
        - FROM_NAME
        - TO_FILE
        - FROM_FILE
    """
    TO_NAME = '\\\\.\\pipe\\ToSrvPipe'
    FROM_NAME = '\\\\.\\pipe\\FromSrvPipe'
    
    TO_FILE: None | TextIOWrapper = None
    FROM_FILE: None | TextIOWrapper = None

AFA = AudacityFileAccess()

def create_pipe():
    """
    Establish the connection between LPRT & Audacity.
    
        Will raise an `AudacityPipelineError` when the pipe can't be accessed.
    """
    print("-- Both pipes exist.  Good.")

    #AFA.TO_FILE = open(AFA.TO_NAME, 'w')
    

    AFA.TO_FILE = win32file.CreateFile(AFA.TO_NAME, 
                              win32file.GENERIC_WRITE,
                              win32file.FILE_SHARE_WRITE,
                              None,
                              win32file.OPEN_EXISTING,
                              win32file.FILE_ATTRIBUTE_NORMAL,
                              0)
    print("-- File to write to has been opened")
    """
    On the testsystem(Windows 11) the connection to the mod-pipe will be established only:
    When The following code does its thing!
    Make sure Audacity is running!
    """
    AFA.FROM_FILE = win32file.CreateFile(AFA.FROM_NAME, 
                              win32file.GENERIC_READ,
                              win32file.FILE_SHARE_READ,
                              None,
                              win32file.OPEN_EXISTING,
                              win32file.FILE_ATTRIBUTE_NORMAL,
                              0)

    print(f"-- Opened {AFA.FROM_NAME}")

def break_pipe():
    win32file.CloseHandle(AFA.TO_FILE)
    win32file.CloseHandle(AFA.FROM_FILE)
    AFA.TO_FILE.close()
    AFA.FROM_FILE.close()

def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    while 1:
        try:
            win32file.WriteFile(AFA.TO_FILE,str(command + '\r\n\0').encode())
            win32file.FlushFileBuffers(AFA.TO_FILE)
            break
        except:
            pass

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        try:
            line = win32file.ReadFile(AFA.TO_FILE,10)
            line = AFA.FROM_FILE.readline()
            if line == '\n' and len(result) > 0:
                break
        except:
            break
    return 1

def do_command(command):
    """Send one command, and return the response."""
    
    response = None
    try:
        send_command(command)
        response = get_response()
        print("Rcvd: <<< \n" + response)
    except Exception as E:
        print(E)
    
    return response