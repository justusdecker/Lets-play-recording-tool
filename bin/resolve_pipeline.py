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
                with open(self.davinci_pipe,'w') as file:
                    file.write('')
            with open(self.davinci_pipe,'w') as file:
                file.write(command)
        except PermissionError as E:
            print(E)
    def recvFromFile(self):
        try:
            if not isfile(self.user_pipe):
                with open(self.user_pipe,'w') as file:
                    file.write('')
            with open(self.user_pipe,'r') as file:
                _ret =  file.read()
                return _ret
        except PermissionError as E:
            print(E)