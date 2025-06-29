""""""
from os.path import isfile
from bin.data_access import file_read, file_write
class DaviniciSender:
    def __init__(self):
        self.davinci_pipe = 'E:\\davinciResolve\\dvp.txt'
        self.user_pipe = 'E:\\davinciResolve\\up.txt'
        self.eol = '\r\n\0'
        
    def send_to_file(self,command):
        try:
            if not isfile(self.davinci_pipe):
                file_write(self.davinci_pipe,'')
            file_write(self.davinci_pipe,command)
        except PermissionError as E:
            print(E)
    def recvFromFile(self):
        try:
            if not isfile(self.user_pipe):
                file_write(self.user_pipe,'')
            return file_read(self.user_pipe)
        except PermissionError as E:
            print(E)