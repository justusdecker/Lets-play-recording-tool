__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__version__ = "0.8.4"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from bin.constants import *

from bin.data_access import LetsPlay, isfile, json_write
from bin.others import binpi

from bin.automations import (
    obs_connect,
    create_new_lp_file,
    #fetch_audio,
    #fix_audio,
    #gen_thumbnail,
    #compare_audio_and_render,
    #extract_silence,
    GetSilenceWF,
    GenerateThumbnailWF,
    ExtractAudioWF,
    FixAudioWF,
    CompareAndRenderWF,
    AudioNRWF,
    LP_PATH
)

class App:
    def __init__(self):
        self.isrunning = True
        self.current_letsplay_id = 0 #! will be changed to a setting
        print(color816('',31),end='') # resets the terminal color
    
    def options_submenu(self):
        """
        Main Menu > Options
        """
        while self.isrunning:
            match binpi(menu(MENU_SETTINGS_OPTIONS,'options',exit_name='Back')):
                case 1: #. (1) Create the settings.json > Only if the file not exists
                    if isfile('settings.json'):
                        err(ERROR_002)
                        continue
                    
                    json_write('settings.json',DEFAULT_OBS_SETTINGS)
                case 2:#. (2) Change Lets Play ID
                    l = len(LetsPlay(LP_PATH).get_names())
                    tmp = binpi(f'Enter a value from 0 to {l-1}','set lp_id: ')
                    
                    if tmp < l:
                        self.current_letsplay_id = tmp
                    else:
                        err(ERROR_001)
                        continue
                case 3: #. (3) Create the default_tad.json > Only if the file not exists
                    if isfile('default_tad.json'):
                        err(ERROR_002)
                        continue
                    json_write('default_tad.json',DEFAULT_TAD)
                case 4: #. (4) Create a new Lets Play File > IF not exist
                    create_new_lp_file()
                case 0: #+ Returns to the main menu
                    return
                case _: #! Error occured - User input is not in option range
                    err(ERROR_003)
    
    def main_menu(self):
        """
        Main Menu >
        """
        match binpi(menu(MENU_OPTIONS,'main')):
            case 1: #. (1) OBS - Recording >  Will save your recording data to the in lets_play.csv referrenced episode file
                ep = LetsPlay(LP_PATH).get_episodes(self.current_letsplay_id)
                obs_connect(ep)
            case 2: #. (2) Select the automation submenu
                self.automation_sub_menu()
            case 3: #. (3) Deploy
                nimp()
            case 4: #. (4) Select the options submenu
                self.options_submenu()
            case 0: #+ Close the app
                self.isrunning = False
            case _: #! Error occured - User input is not in option range
                err(ERROR_003)
    
    def automation_sub_menu(self):
        while self.isrunning:
            match binpi(menu(MENU_AUTOMATION_OPTIONS,'automations',exit_name='Back')):
                case 1: #. (1) Thumbnail Generator
                    GenerateThumbnailWF()
                case 2: #. (2) Audio Extraction
                    ExtractAudioWF()
                case 3: #. (3) Get Silence
                     GetSilenceWF()
                case 4: #. (4) Create Noise profiles
                    AudioNRWF()
                case 5: #. (5) Audio: Limiter , Loudness Normalization & Noise Reduction
                    FixAudioWF()
                case 6: #. (6) User compare audio & rendering
                    CompareAndRenderWF()
                case 0:
                    return
                case _:
                    err(ERROR_003)
                     
    def loop(self):
        while self.isrunning:
            self.main_menu()
            
if __name__ == "__main__":
    APP = App()
    APP.loop()