""""""
from os.path import isfile
from bin.data_access import file_read, file_write
from time import time
# DVRPATH = "C:\Users\Justus\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit"

class DaviniciSender:
    """
    Send Davinci Resolve one of the following instructions:
    
    <$CIMPORT> {filePath} - creates an TimeLine with given Element
    <$IMPORT> {filePath} - Load Element in existing TimeLine
    
    <$DELETETRACK> {id} - Deletes an AudioTrack with given id
    """
    def __init__(self):
        self.davinci_pipe = 'E:\\davinciResolve\\dvp.txt'
        self.user_pipe = 'E:\\davinciResolve\\up.txt'
            
    def send_to_davinci(self,command):
        """
        From user to davinci
        """
        try:
            if not isfile(self.davinci_pipe):
                file_write(self.davinci_pipe,'')
            file_write(self.davinci_pipe,command)
        except PermissionError as E:
            print(E)
  
    def recv_from_user(self):
        """
        Davinci result
        """
        try:
            if not isfile(self.user_pipe):
                return ''
            ret = ''
            _start = time()
            while not ret or time() - _start > 2:
                ret = file_read(self.user_pipe)
            return ret
        except PermissionError as E:
            print(E)
    
    def clean(self,typ: bool):
        file_write(self.davinci_pipe if typ else self.user_pipe,'')