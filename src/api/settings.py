raise NotImplementedError()
from os.path import isfile
from json import load

DEFAULT_SETTINGS = {'lang':'EN'}

class Settings:
    from os import getlogin


    ROOT = f'C:\\Users\\{getlogin()}\\lprt\\'
    del getlogin
    PATH = f'{ROOT}lprt_settings.json'
    def __init__(self):
        self.load()
    def load(self):
        if isfile(self.PATH):
            with open(self.PATH) as f:
                self.settings = load(f)
            
            if not isinstance(self.settings, dict):
                self.settings = DEFAULT_SETTINGS.copy()
        else:
            self.settings = DEFAULT_SETTINGS.copy()
    def update(self,key,val):
        self.settings[key] = val
SETTINGS = Settings()