from bin.obs import OBSObserver
from bin.data_access import Episode, LetsPlay, cnef
from bin.wintoasty import toast_finished

from bin.ffmpeg import *
LP_PATH = 'lets_plays.csv'

from os import getlogin
USERNAME = getlogin()
del getlogin
ROOT = f'C:\\Users\\{USERNAME}\\lprt\\'
AUDIO_FOLDER = f'{ROOT}audio\\'

def obs_connect(ep: Episode,el):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up or a keyboard interrupt happens
    """
    OBSO = OBSObserver()
    if OBSO.failed:
        el.btn_connect.configure(text= 'Settings File does not exist!')
        return
    if not OBSO.isconnected:
        el.btn_connect.configure(text= 'No Connection!')
        return
    while OBSO.isconnected:
        el.btn_connect.configure(text= 'Connection established')
        try:
            el.label.configure(text= OBSO.timecode)
            OBSO.update(ep)
        except:
            el.btn_connect.configure(text= 'Unexpected Error happened')
            print('Unexpected Error happened')


class GenericWorkFlow:
    def __init__(self, folder: str, finish_message: str):
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        self.run()
    
    @property
    def rng(self) -> tuple[int,int]:
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
    
    def run(self,lpid: int,ep_range: list[int,int]):
        cnef(self.auto_create_folder_path)
        self.letsplay = LetsPlay(LP_PATH)

        self.lpid,self.epr = lpid,ep_range
        self.lp_name = self.letsplay.get_name(self.lpid)
        self.ep_path = self.letsplay.get_episode_path(self.lpid)
        self.episode = Episode(self.ep_path)
        
    def user_workflow(self):
        toast_finished(self.finish_message)
    

class ExtractAudioWF(GenericWorkFlow):#! bin.constants throws an exception bold NameError
    """
    Audio Extraction from Video
    """
    def __init__(self):
        super().__init__(folder=AUDIO_FOLDER, finish_message='Audio extraction finished')
        self.user_workflow()
    def user_workflow(self):
        for i in range(*self.rng): 
            video_path = self.episode.get_video_path(i)
                                
            t1_path, t2_path = f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic.aac',f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_desktop.aac'
            
            #inf(f'Start extract tracks from {video_path}')

            ffmpeg_run(FFMPEG_OPTIMIZED_EXTRACT,{'__IN__':video_path,'__OUT1__':t1_path, '__OUT2__':t2_path})

            self.episode.set_audio_mic_path(i,t1_path)
            self.episode.set_audio_desktop_path(i,t2_path)
            
            self.episode.save()
        super().user_workflow()