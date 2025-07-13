__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.9.54"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Production"

"""
To enable the Audacity pipeline:
Open Audacity
Edit > Settings > Module > enable mod-script-pipe
Reopen Audacity & Reopen LPRT(If open)
"""


from os.path import exists
class AudacityPipelineError(Exception):
    pass

TO_NAME = '\\\\.\\pipe\\ToSrvPipe'
FROM_NAME = '\\\\.\\pipe\\FromSrvPipe'
EOL = '\r\n\0'

print("Write to  \"" + TO_NAME +"\"")
if not exists(TO_NAME):
    raise AudacityPipelineError(f"{TO_NAME} ..does not exist. Ensure Audacity is running with mod-script-pipe.")

print("Read from \"" + FROM_NAME +"\"")
if not exists(FROM_NAME):
    raise AudacityPipelineError(f"{FROM_NAME} ..does not exist. Ensure Audacity is running with mod-script-pipe.")

print("-- Both pipes exist.  Good.")

TO_FILE = open(TO_NAME, 'w')
print("-- File to write to has been opened")
FROM_FILE = open(FROM_NAME, 'rt')
print(f"-- Opened {FROM_NAME}")

def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TO_FILE.write(command + EOL)
    TO_FILE.flush()

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROM_FILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    """Send one command, and return the response."""
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

#do_command('Help: Command=Help')