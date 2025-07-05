__author__ = "Justus Decker"
__copyright__ = "(c) 2024 - 2025 , The LPRT Project"
__credits__ = []
__license__ = "CC BY-NC-ND"
__version__ = "0.3.118"
__maintainer__ = "Justus Decker"
__email__ = "justus.d2025@gmail.com"
__status__ = "Testing"

from bin.constants import *

from bin.data_access import LetsPlay, cnef, isfile, Episode,json_write
from bin.others import binpi, input_episode_range


from bin.automations import (
    obs_connect,
    create_new_lp_file,
    fetch_audio,
    fix_audio,
    gen_thumbnail,
    LP_PATH
)

from bin.audio_player import AudioPlayer

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
            match binpi(MENU_OPTIONS_MESSAGE):
                case 1:
                    """
                    (1) Create the settings.json
                    Only if the file not exists
                    """
                    if isfile('settings.json'):
                        err(ERROR_002)
                        continue
                    
                    json_write('settings.json',DEFAULT_OBS_SETTINGS)
                case 2:
                    """
                    
                    """
                    l = len(LetsPlay(LP_PATH).get_names())
                    tmp = binpi(f'Enter a value from 0 to {l-1}','set lp_id: ')
                    
                    if tmp < l:
                        self.current_letsplay_id = tmp
                    else:
                        err(ERROR_001)
                        continue
                case 3:
                    """
                    (3) Create the default_tad.json
                    Only if the file not exists
                    """
                    if isfile('default_tad.json'):
                        err(ERROR_002)
                        continue
                    json_write('default_tad.json',DEFAULT_TAD)
                case 4:
                    create_new_lp_file()
                case 0:
                    return
                case _:
                    err(ERROR_003)
    
    def main_menu(self):
        """
        Main Menu >
        """
        match binpi(MENU_MESSAGE):
            case 1:
                # OBS - Recording
                # Will save your recording data to the in lets_play.csv referrenced episode file
                ep = LetsPlay(LP_PATH).get_episodes(self.current_letsplay_id)
                obs_connect(ep)
            case 2:
                self.automation_sub_menu()
            case 3:
                nimp()
            case 4:
                self.options_submenu()
            case 0:
                self.isrunning = False
            case _:
                err(ERROR_003)
    
    def automation_sub_menu(self):
        while self.isrunning:

            match binpi(MENU_AUTOMATION_MESSAGE):
                case 1:
                    """
                    (1) Thumbnail Generator
                    """
                    gen_thumbnail()
                case 2:
                    """
                    (2) Audio Fetch
                    Get all video - audio track 1 & 2
                    """
                    cnef(AUDIO_FOLDER)
                    letsplay = LetsPlay(LP_PATH)
                    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
                    if res is not None:
                        lp,epr = res
                        lp_name = letsplay.get_name(lp)
                        ep_path = letsplay.get_episode_path(lp)
                        if epr[0] == epr[1]:
                            fetch_audio(Episode(ep_path),epr[0],lp_name)
                        else:
                            episode = Episode(ep_path)
                            for i in range(epr[0],epr[1]):
                                fetch_audio(episode,i,lp_name)
                case 3:
                    """
                    (3) Audio Fix / Edit
                    """
                    fix_audio()
                case 4:
                    """
                    Audio Compare
                    
                    """
                    
                    letsplay = LetsPlay(LP_PATH)
                    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
                    if res is not None:
                        lp,epr = res
                        ep_path = letsplay.get_episode_path(lp)
                        ep = Episode(ep_path)
                        if epr[0] == epr[1]:
                            mic = ep.get_audio_mic_path(epr[0])
                            desk = ep.get_audio_desktop_path(epr[0])
                            
                            AP = AudioPlayer(mic, desk)
                            AP.run()
                            volume = AP.vol
                            del AP

                                
                            print(mic,desk,volume)
                        else:
                            for i in range(epr[0],epr[1]):
                                mic = ep.get_audio_mic_path(i)
                                desk = ep.get_audio_desktop_path(i)
                                inf(f'{mic} {desk}')
                                AP = AudioPlayer(mic, desk)
                                AP.run()
                                volume = AP.vol
                                del AP
                                        
                                print(mic,desk,volume)
                case 5:
                    pass  
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