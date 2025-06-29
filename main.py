
from bin.constants import *
from bin.obs import OBSObserver
from bin.data_access import LetsPlay, file_read, isfile, LP_KEYS, EP_KEYS, file_write,csv_write, Episode,json_write
from tkinter.filedialog import asksaveasfilename as asafn, askopenfilename as aofn
from bin.others import binpi,binps, input_episode_range
from bin.thumbnail import ThumbnailGenerator
from bin.audio import extract_audio, loudness_normalization, limiter

LP_PATH = 'lets_plays.csv'
def obs_connect(ep: Episode):
    OBSO = OBSObserver()
    if not OBSO.isconnected:
        err(ERROR_004)
    while OBSO.isconnected:
        try:
            print(OBSO.timecode)
            OBSO.update(ep)
            
        except KeyboardInterrupt:
            err(ERROR_005)
            break

def create_new_lp_file():
    print(color816(f'[!TIP] > If you have a typo somewhere: You can change the data later manually!(Do it or bugs will kill your fun :D)',32))
    if not isfile(LP_PATH):
        csv_write(LP_PATH,[[binps(f'{key}: ') if key != 'version' else file_read('version.txt') for key in LP_KEYS]])
    else:
        err(ERROR_002)

def create_new_ep_file(filepath: str):
    print(color816(f'[!TIP] > If you have a typo somewhere: You can change the data later manually!(Do it or bugs will kill your fun :D)',32))
    
    if not isfile(filepath):
        csv_write(filepath,[[binps(f'{key}: ') for key in EP_KEYS]])
    else:
        err(ERROR_002)

def fetch_audio(episode: Episode,i: int,lp_name: str):
    video_path = episode.get_video_path(i)
                                
    t1_path, t2_path = f'{i+1}_{lp_name}_track_mic.mp3',f'{i+1}_{lp_name}_track_desktop.mp3'
    
    inf(f'Start extract track 1 from {t1_path}')
    extract_audio(video_path,t1_path,1)

    inf(f'Start extract track 2 from {t2_path}')
    extract_audio(video_path,t2_path,2)

    
def fix_audio(episode: Episode,i: int, lp_name):

    audio_mic_path = episode.get_audio_mic_path(i)
    audio_desktop_path = episode.get_audio_desktop_path(i)
    
    t1_path, t2_path = f'{i+1}_{lp_name}_track_mic_ln.mp3',f'{i+1}_{lp_name}_track_desktop_ln.mp3'
    
    t3_path, t4_path = f'{i+1}_{lp_name}_track_mic_fixed.mp3',f'{i+1}_{lp_name}_track_desktop_fixed.mp3'
    
    inf(f'Start normalize track 1 to {t1_path}')
    loudness_normalization(audio_mic_path, t1_path)
    
    inf(f'Start limit track 1 to {t3_path}')
    limiter(t1_path, t3_path)
    
    inf(f'Start normalize track 2 to {t2_path}')
    loudness_normalization(audio_desktop_path, t2_path)
    
    inf(f'Start limit track 2 to {t4_path}')
    limiter(t2_path, t4_path)

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
                    
                    res = input_episode_range(letsplay.get_episode_ammount(),letsplay.get_names())
                    if res is not None:
                        lp,epr = res
                        lp_name = letsplay.get_name(lp)
                        ep_path = letsplay.get_episode_path(lp)
                        if epr[0] == epr[1]:
                            video_path = Episode(ep_path).get_video_path(epr[0])
                            tad = aofn(filetypes=[['JSON','*.json']])
                            if not tad:
                                return
                            TG.generate(
                                str(epr[0]+1),
                                video_path,
                                tad,
                                f'{epr[0]+1}_{lp_name}_thumbnail.png'
                                )
                            
                        else:
                            ep = Episode(ep_path)
                            tad = aofn(filetypes=[['JSON','*.json']])
                            if not tad:
                                return
                            
                            for i in range(epr[0],epr[1]):
                                video_path = ep.get_video_path(i)
                                TG.generate(
                                str(i+1),
                                video_path,
                                tad,
                                f'{i+1}_{lp_name}_thumbnail.png'
                                )
                case 2:
                    """
                    (2) Audio Fetch
                    Get all video - audio track 1 & 2
                    """
                    
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