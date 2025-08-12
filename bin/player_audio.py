from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

from tkinter import Toplevel, DoubleVar, LEFT
from tkinter.ttk import Button, Label, LabeledScale
from bin.ffmpeg import ffmpeg_run, FFMPEG_AUDIO_COMBINE_TRUNCATED
from bin.constants import TEMP_FOLDER

try: #Fix for issue: #126
    from pygame.mixer import init, music
except:
    from tkinter.messagebox import showerror
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\npygame')
    quit()

init()
from bin.media_player import MediaPlayer
class AudioPlayer(MediaPlayer):
    def __init__(self, paths, app):
        self.audio_list = paths
        self.current_episode = 0
        self.isfinished = False
        super().__init__(app, True)
        
        self.finished_button = Button(self.bar,text='Apply Volume', command=self.destroy)
        self.finished_button.pack(side=LEFT)
        self.finished_all_button = Button(self.bar,text='Apply Volume to\nall episodes!', command=self.destroy)
        self.finished_all_button.pack(side=LEFT)
    @property
    def current_media(self) -> list:
        return self.audio_list[self.current_episode]
    
    @property
    def media(self) -> str:
        ffmpeg_run(FFMPEG_AUDIO_COMBINE_TRUNCATED,{
            '__IN1__':self.current_media[1],
            '__IN2__': self.current_media[2],
            '__VOLUME1__': str(1.0),
            '__VOLUME2__': str(self.current_media[4]),
            '__OUT__':f'{TEMP_FOLDER}temp.mp3'})
        return f'{TEMP_FOLDER}temp.mp3'
    
    def episode_down(self,*args):
        """ Change the selected episode. One down. """
        new_location = self.current_episode - 1

        if new_location < 0:
            self.current_episode = 0
        else:
            self.current_episode = new_location

            self.set_title()
            self.open_file(self.media)
            self.play_video()
            
    def episode_up(self,*args):
        """ Change the selected episode. One up. """
        new_location = self.current_episode + 1
        
        l = len(self.data)
        
        if new_location > l - 1:
            self.current_episode = l - 1
        else:
            self.current_episode = new_location
            self.set_title()
            self.open_file(self.media)
            self.play_video()
    def set_volume(self, value):
        super().set_volume(value)
        self.current_media[4] = self.vol
    def destroy(self):
        super().destroy()
        self.isfinished = True