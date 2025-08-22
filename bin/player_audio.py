from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

from tkinter import LEFT, Scale, HORIZONTAL
from tkinter.ttk import Button
from bin.ffmpeg import ffmpeg_run, FFMPEG_AUDIO_COMBINE_TRUNCATED
from bin.constants import TEMP_FOLDER
from tools.log import *
from bin.ui import change_states
from bin.media_player import NewMediaPlayer

class NewAudioPlayer(NewMediaPlayer):
    def __init__(self, parent, paths, app):
        self.audio_list = paths
        self.current_episode = 0
        self.isfinished = False
        self.busy_state = False
        self.desktop_vol = 1.
        super().__init__(parent, app, True)
        
        self.finished_button = Button(self.bar,text='Apply Volume', command=app.run_automation)
        self.finished_button.pack(side=LEFT)
        self.finished_all_button = Button(self.bar,text='Set Volume for\nall episodes!', command=self.apply_vol_to_all)
        self.finished_all_button.pack(side=LEFT)
        
        self.desktop_volume_slider = Scale(
            self.controls, from_=0, to=100,
            orient=HORIZONTAL, label="Desktop Volume",
            command=self.set_volume_desktop
        )
        
        self.desktop_volume_slider.set(50)  # Set the default volume to 50%
        self.desktop_volume_slider.pack(side=LEFT, padx=5)
    
    def reset(self,al):
        self.player.stop()
        self.audio_list = al
        self.current_episode = 0
        self.isfinished = False
        self.busy_state = False
        self.desktop_vol = 1.
        self.play_video()
    
    def get_ui(self):
        return [self.finished_all_button,self.finished_button, self.last_button,self.next_button,self.play_button,self.pause_button,self.stop_button]
    
    @property
    def current_media(self) -> list:
        if self.audio_list:
            return self.audio_list[self.current_episode]
        else:
            return []
    
    @property
    def media(self) -> str:
        if not self.audio_list: return ''
        
        change_states([self.stop_button,self.play_button, self.pause_button, self.next_button, self.last_button,self.finished_all_button, self.finished_button],'disabled')
        self.busy_state = True
        LOG('Start combining $($) & $($)',[self.current_media[1],1.0,self.current_media[2],self.current_media[4]])
        ffmpeg_run(FFMPEG_AUDIO_COMBINE_TRUNCATED,{
            '__IN1__':self.current_media[1],
            '__IN2__': self.current_media[2],
            '__VOLUME1__': str(1.0),
            '__VOLUME2__': str(self.current_media[4]),
            '__OUT__':f'{TEMP_FOLDER}temp.mp3'})
        LOG(f'Finished combining $',[f'{TEMP_FOLDER}temp.mp3'])
        change_states([self.stop_button,self.play_button, self.pause_button, self.next_button, self.last_button,self.finished_all_button, self.finished_button],'!disabled')
        self.busy_state = False
        return f'{TEMP_FOLDER}temp.mp3'
    
    def episode_down(self,*args):
        """ Change the selected episode. One down. """
        
        new_location = self.current_episode - 1

        if new_location < 0:
            self.current_episode = 0
            LOG('Cannot change episode',logtype=LOG_WARNING)
        else:
            self.current_episode = new_location
            LOG(f'Changed episode to {new_location}')
            self.play_video()
             
    def episode_up(self,*args):
        """ Change the selected episode. One up. """
        new_location = self.current_episode + 1
        
        l = len(self.audio_list)
        
        if new_location > l - 1:
            self.current_episode = l - 1
            LOG('Cannot change episode',logtype=LOG_WARNING)
        else:
            self.current_episode = new_location
            LOG(f'Changed episode to {new_location}')
            self.play_video()
            
    def play_video(self):
        self.open_file()
        LOG('Start playing',logtype=LOG_INFO)
        self.current_media_label.configure(text=f'{self.current_media[0]+1}')
        return super().play_video()
    
    def open_file(self):
        
        return super().open_file(self.media)
    
    def set_volume_desktop(self, value):
        if self.busy_state: return
        if not self.audio_list: return
        self.desktop_vol = int(value)
        self.current_media[4] = self.desktop_vol / 100 if self.desktop_vol else 0
        
    def apply_vol_to_all(self):
        if not self.audio_list: return
        for media in self.audio_list:
            media[4] = self.desktop_vol