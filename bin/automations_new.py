from bin.obs import OBSObserver
from bin.data_access import Episode, LetsPlay, cnef
from bin.wintoasty import toast_finished

from bin.ffmpeg import *
from bin.audacity_pipeline import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox as msgbox
from os import listdir
LP_PATH = 'lets_plays.csv'

from os import getlogin
USERNAME = getlogin()
del getlogin
ROOT = f'C:\\Users\\{USERNAME}\\lprt\\'
AUDIO_FOLDER = f'{ROOT}audio\\'
TEMP_FOLDER = f'{ROOT}temp\\'
THUMBNAIL_FOLDER = f'{ROOT}thumbnails\\'
FIXED_AUDIO_FOLDER = f'{ROOT}audio_fixed\\'

#This is the start of a fix for issue #78
cnef(AUDIO_FOLDER)
cnef(FIXED_AUDIO_FOLDER)
cnef(TEMP_FOLDER)
cnef(THUMBNAIL_FOLDER)

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
    def __init__(self, folder: str, finish_message: str,lpid,epr):
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        
        self.letsplay = LetsPlay(LP_PATH)
        self.lpid,self.epr = lpid,epr
        self.lp_name = self.letsplay.get_name(self.lpid)
        self.ep_path = self.letsplay.get_episode_path(self.lpid)
        self.episode = Episode(self.ep_path)
    @property
    def rng(self) -> tuple[int,int]:
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
        
    def user_workflow(self):
        toast_finished(self.finish_message)
    

class ExtractAudioWF(GenericWorkFlow):#! bin.constants throws an exception bold NameError
    """
    Audio Extraction from Video
    """
    def __init__(self,lpid,epr,app):
        super().__init__(folder=AUDIO_FOLDER, finish_message='Audio extraction finished',lpid=lpid,epr=epr)
        self.user_workflow(app)
    def user_workflow(self,app):
        for i in range(*self.rng): 
            video_path = self.episode.get_video_path(i)
                       
            t1_path, t2_path = f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic.aac',f'{AUDIO_FOLDER}{i+1}_{self.lp_name}_track_desktop.aac'
            
            ffmpeg_run(FFMPEG_OPTIMIZED_EXTRACT,{'__IN__':video_path,'__OUT1__':t1_path, '__OUT2__':t2_path})
            app.pb.step((1 / (self.rng[1] + 1))*100)
            self.episode.set_audio_mic_path(i,t1_path)
            self.episode.set_audio_desktop_path(i,t2_path)
            
            self.episode.save()

        app.start_btn.state(['!disabled'])
        super().user_workflow()


class FixAudioWF(GenericWorkFlow):
    """
    Fixes your mic recording
    
    Uses filters:
    - Lowpass
    - Highpass
    - Loudness Normalize
    - Limiter
    """
    def __init__(self,lpid, epr,app):
        super().__init__(FIXED_AUDIO_FOLDER, 'Audio Fix', lpid, epr)
        self.user_workflow(app)
        
    def user_workflow(self,app):
        
        for i in range(*self.rng): 
            audio_mic_path = self.episode.get_audio_mic_path(i)
            
            dest = f'{FIXED_AUDIO_FOLDER}{i+1}_{self.lp_name}_track_mic_fixed.aac'
            
            cnef(TEMP_FOLDER)
            
            ffmpeg_run(FFMPEG_AUDIO_PF_LN_L,{'__IN__': audio_mic_path,'__OUT__':dest})
            app.pb.step((1 / (self.rng[1] + 1))*100)
            self.episode.set_audio_mic_edit1_path(i,dest)
            self.episode.save()
        app.start_btn.state(['!disabled'])
        super().user_workflow()


class SendToAudacityWF(GenericWorkFlow):
    """
    Generating Thumbnails based on the thumbnail automation data
    """
    def __init__(self,lpid, epr,app):
        super().__init__(folder = THUMBNAIL_FOLDER, finish_message = 'Audacity Send',lpid=lpid, epr=epr)
        self.user_workflow(app)
    def user_workflow(self, app):
        try:
            create_pipe()
        except:
            msgbox.showerror('ERROR','Did you open Audacity & enabled the mod-pipe?')
            app.start_btn.state(['!disabled'])
            return
        ui = msgbox.askyesno('LPRT to AC','Do you want to send data to Audacity?')
        
        if ui:
            
            for i in range(*self.rng): 
                filepath = self.episode.get_audio_mic_edit1_path(i)
                if do_command(f'Import2: filename="{filepath}"') is None:
                    msgbox.showerror('ERROR','Audacity is not reachable!')
                    app.start_btn.state(['!disabled'])
                    return
                app.pb.step((1 / (self.rng[1] + 1))*100)
                #! The Noise Reduction is not automated
        toast_finished('Finished Importing')
        results_path = askdirectory() + '/'
        files = listdir(results_path)
        if self.episode.row != len(files):
            msgbox.showerror('ERROR','Did you miss some episodes?')
            app.start_btn.state(['!disabled'])
            return
        for file in files:
            ep = int(file.split('_-')[1].split('.')[0]) - 1
            old = results_path + file
            new = old.split('.')[0] + '.aac'
            ffmpeg_run(FFMPEG_CONVERT_AUDIO_TYPE,{'__IN__': old, '__OUT__': new})
            #remove()
            self.episode.set_audio_mic_edit2_path(ep, new)
            self.episode.save()
        app.start_btn.state(['!disabled'])
        super().user_workflow()