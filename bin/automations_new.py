"""
This Module does generate on start all essential paths & contains all automations e.g. FetchAudioWF


Contains:
- GenericWorkFlow
- ThumbnailGenerator
- FetchAudio
- FixAudio
- Send2Audacity
- CompAndRender
"""


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
VIDEO_FOLDER = f'{ROOT}video\\'
TAD_FOLDER = f'{ROOT}tad\\'
TEMP_FOLDER = f'{ROOT}temp\\'
THUMBNAIL_FOLDER = f'{ROOT}thumbnails\\'
FIXED_AUDIO_FOLDER = f'{ROOT}audio_fixed\\'

# fix for issue #78
cnef(AUDIO_FOLDER)
cnef(FIXED_AUDIO_FOLDER)
cnef(THUMBNAIL_FOLDER)
cnef(VIDEO_FOLDER)
cnef(TAD_FOLDER)
cnef(TEMP_FOLDER)

from tkinter import Toplevel
from tkinter.ttk import Button, LabeledScale, Label
from bin.lprtplay import play_audio, stop_audio
from tkinter import DoubleVar

class AudioPlayer(Toplevel):
    """
    A Tkinter Toplevel window that functions as a simple audio player.

    This player allows users to play, stop, and navigate through a list of audio
    files. It also provides a volume control and displays the current episode
    number. The audio playback functionality relies on external functions
    `stop_audio`, `ffmpeg_run`, and `play_audio`.
    """
    def __init__(self,paths):
        
        self.audio_list = paths
        print(len(paths))
        self.current_episode = 0
        super().__init__()
        self.isfinished = False
        self.title('Test')
        self.geometry('300x200')
        self.vol = DoubleVar(self,1.0)
        self.volume_slider = LabeledScale(self,self.vol,from_=0.0,to=1.0)
        self.volume_slider.grid(row=0,column=0)
        
        self.play_button = Button(self,text='Play',command=self.play)
        self.play_button.grid(row=1,column=0)
        
        self.stop_button = Button(self,text='Stop',command=self.stop)
        self.stop_button.grid(row=2,column=0)
        self.stop_button.state(['disabled'])
        
        self.down_button = Button(self,text='Down',command=self.episode_down)
        self.down_button.grid(row=3,column=0)
        
        self.curr_ep_label = Label(self,text='')
        self.curr_ep_label.grid(row=3,column=1)
        
        self.up_button = Button(self,text='Up',command=self.episode_up)
        self.up_button.grid(row=3,column=2)
        
        self.finished_button = Button(self,text='Finished', command=self.byebye)
        self.finished_button.grid(row=4,column=0)
    def stop(self,*args):
        """Stops the currently playing audio and updates button states."""
        self.stop_button.state(['disabled'])
        self.play_button.state(['!disabled'])
        stop_audio()
        
    def play(self, *args):
        """Plays the audio for the current episode."""
        print(self.audio_list[self.current_episode])
        self.stop_button.state(['!disabled'])
        self.play_button.state(['disabled'])
        stop_audio()
        ffmpeg_run(FFMPEG_AUDIO_COMBINE_TRUNCATED,{'__IN1__':self.audio_list[self.current_episode][1],'__IN2__': self.audio_list[self.current_episode][2],'__VOLUME1__': str(1.0),'__VOLUME2__': str(self.audio_list[self.current_episode][4]),'__OUT__':'temp.mp3'})
        play_audio('temp.mp3')
        
    def byebye(self, *args):
        """Closes the AudioPlayer window and sets the `isfinished` flag to True."""
        self.destroy()
        self.isfinished = True
    def get_volume(self) -> float:
        """Retrieves the current volume level from the volume slider."""
        return float(f'{self.vol.get():.2f}')
    
    def episode_down(self,*args):
        """
        Navigates to the previous audio episode in the list.

        If the current episode is already the first one, it stays at index 0.
        It updates the current episode index, saves the current volume for the
        new episode, and updates the episode label.
        """
        new_location = self.current_episode - 1

        if new_location < 0:
            self.current_episode = 0
        else:
            self.current_episode = new_location
        self.audio_list[self.current_episode][4] = self.get_volume()
        self.curr_ep_label.configure(text=f'{self.current_episode}')
            
    def episode_up(self,*args):
        """
        Navigates to the next audio episode in the list.

        If the current episode is already the last one, it stays at the last index.
        It updates the current episode index, saves the current volume for the
        new episode, and updates the episode label.
        """
        new_location = self.current_episode + 1
        
        l = len(self.audio_list)
        
        if new_location > l - 1:
            self.current_episode = l - 1
            

        else:
            self.current_episode = new_location
        self.audio_list[self.current_episode][4] = self.get_volume()
        self.curr_ep_label.configure(text=f'{self.current_episode}')
        
def obs_connect(ep: Episode,el):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up
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
        """
        Initializes a GenericWorkFlow instance, setting up paths, messages,
        and "LetsPlay" episode-related attributes.

        This class serves as a base for workflows that interact with the `LetsPlay` class, 
        managing episode-specific data and providing a windows toast message
        to signal workflow completion.
        """
        self.auto_create_folder_path = folder
        self.finish_message = finish_message
        
        self.letsplay = LetsPlay(LP_PATH)
        self.lpid,self.epr = lpid,epr
        self.lp_name = self.letsplay.get_name(self.lpid)
        self.ep_path = self.letsplay.get_episode_path(self.lpid)
        self.episode = Episode(self.ep_path)
    @property
    def rng(self) -> tuple[int,int]:
        """
        Returns the effective episode range as a tuple (start, end).

        The end of the range is inclusive. If the start and end episodes
        in `epr` are the same, the end of the returned range is incremented by 1
        to ensure a valid range for iteration (e.g., (5,5) becomes (5,6)).

        Returns:
            tuple[int, int]: A tuple representing the (start_episode, end_episode)
                             for the workflow.
        """
        return self.epr[0],self.epr[1]+(1 if self.epr[0] == self.epr[1] else 0)
        
    def user_workflow(self):
        """
        Executes the primary user-facing part of the workflow.

        This method currently triggers a 'toast' notification indicating
        the workflow has finished, using the provided `finish_message`
        """
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

class CompareAndRenderWF(GenericWorkFlow):
    """
    CAAR
    ---
    Audio Compare & render the results at the end
    
    Uses FFMPEG to edit audio & render video in bulk.
    
    
    .. render_queue::
        Because rendering takes a long time the paths will be stored temporary in this list. Formatted like: (video, audio, index)
    
    .. result_file_path::
        **AUDIO_FOLDER/**{`ep_index` + `1`}_{`name`}_final.mp3
    """
    def __init__(self,lpid, epr,app):
        super().__init__(folder=TEMP_FOLDER, finish_message="CAAR",lpid=lpid, epr=epr)
        self.user_workflow(app)
    def user_workflow(self,app):
        
        rendering_queue = []

        paths = [[i, self.episode.get_audio_mic_edit1_path(i), self.episode.get_audio_desktop_path(i), self.episode.get_video_path(i),1.0] for i in range(*self.rng)]

        volap = AudioPlayer(paths)
        while not volap.isfinished:
            pass
        result = volap.audio_list
        
        for i, mic, desk, vid, vol in result:
            tmp_audio_path = f'{TEMP_FOLDER}temp_{i+1}_audio_final.mp3'

            ffmpeg_run(
                FFMPEG_AUDIO_COMBINE,
                {
                    '__IN1__':mic,
                    '__IN2__': desk,
                    '__VOLUME1__': str(1.0),
                    '__VOLUME2__': str(vol),
                    '__OUT__':tmp_audio_path
                    }
                )
            rendering_queue.append((vid, tmp_audio_path, i))
        toast_finished("[1/2] Audio combine")   

        path_ending = f'_{self.letsplay.get_game_name(self.lpid)}_final.mp4'
        cnef(VIDEO_FOLDER)
        for video, audio, index in rendering_queue:
            final_path = f'{VIDEO_FOLDER}{index+1}{path_ending}'

            ffmpeg_run(
                FFMPEG_VIDEO_RENDER,
                {
                    '__VIDEO__': video,
                    '__AUDIO__': audio,
                    '__OUTPUT__': final_path
                }
            )
            app.pb.step((1 / (self.rng[1] + 1))*100)
            self.episode.set_final_video_path(index,final_path)
            self.episode.save()
        super().user_workflow()