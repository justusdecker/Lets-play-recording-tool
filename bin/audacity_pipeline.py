__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.10.73"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Production"
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

from io import TextIOWrapper
from os.path import exists
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

EOL = '\r\n\0'
def create_pipe():
    """
    Establish the connection between LPRT & Audacity.
    
        Will raise an `AudacityPipelineError` when the pipe can't be accessed.
    """
    print("Write to  \"" + AFA.TO_NAME +"\"")
    if not exists(AFA.TO_NAME):
        raise AudacityPipelineError(f"{AFA.TO_NAME} ..does not exist. Ensure Audacity is running with mod-script-pipe.")

    print("Read from \"" + AFA.FROM_NAME +"\"")
    if not exists(AFA.FROM_NAME):
        raise AudacityPipelineError(f"{AFA.FROM_NAME} ..does not exist. Ensure Audacity is running with mod-script-pipe.")

    print("-- Both pipes exist.  Good.")

    AFA.TO_FILE = open(AFA.TO_NAME, 'w')
    print("-- File to write to has been opened")
    AFA.FROM_FILE = open(AFA.FROM_NAME, 'rt')
    print(f"-- Opened {AFA.FROM_NAME}")
def break_pipe():
    AFA.TO_FILE.close()
    AFA.FROM_FILE.close()

def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    AFA.TO_FILE.write(command + EOL)
    AFA.TO_FILE.flush()

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = AFA.FROM_FILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    """Send one command, and return the response."""
    
    response = None
    try:
        create_pipe()
        send_command(command)
        response = get_response()
        print("Rcvd: <<< \n" + response)
    except Exception as E:
        print(E)
    
    return response