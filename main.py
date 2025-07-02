
from bin.constants import *

from bin.data_access import LetsPlay, cnef, isfile, Episode,json_write
from tkinter.filedialog import askopenfilename as aofn
from bin.others import binpi, input_episode_range
from bin.thumbnail import ThumbnailGenerator

from bin.automations import (
    obs_connect,
    create_new_lp_file,
    fetch_audio,
    fix_audio,
    gen_thumbnail,
    LP_PATH
)

class App:
    def __init__(self):
        self.isrunning = True
        self.current_letsplay_id = 0
    
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
                    letsplay = LetsPlay(LP_PATH)
                    
                    TG = ThumbnailGenerator()
                    cnef(THUMBNAIL_FOLDER)
                    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
                    if res is not None:
                        lp,epr = res
                        lp_name = letsplay.get_name(lp)
                        ep_path = letsplay.get_episode_path(lp)
                        eps = Episode(ep_path)
                        inf('Please answer the filedialog')
                        tad = aofn(filetypes=[['JSON','*.json']])
                        if epr[0] == epr[1]:
                            video_path = eps.get_video_path(epr[0])
                            gen_thumbnail(TG,lp_name,eps,epr[0],tad)
                            
                        else:
                            
                            for i in range(epr[0],epr[1]):
                                video_path = eps.get_video_path(i)
                                gen_thumbnail(TG,lp_name,eps,i,tad)
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
                    cnef(FIXED_AUDIO_FOLDER)
                    letsplay = LetsPlay(LP_PATH)
                    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
                    if res is not None:
                        lp,epr = res
                        lp_name = letsplay.get_name(lp)
                        ep_path = letsplay.get_episode_path(lp)
                        if epr[0] == epr[1]:
                            fix_audio(ep_path,epr[0],lp_name)
                        else:
                            ep = Episode(ep_path)
                            for i in range(epr[0],epr[1]):
                                fix_audio(ep,i,lp_name)
                case 4:
                    nimp()
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