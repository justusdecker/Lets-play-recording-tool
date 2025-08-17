from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

from tkinter import LEFT, Scale, HORIZONTAL
from tkinter.ttk import Button
from bin.ffmpeg import ffmpeg_run, FFMPEG_AUDIO_COMBINE_TRUNCATED
from bin.constants import TEMP_FOLDER


from bin.media_player import NewMediaPlayer

class NewAudioPlayer(NewMediaPlayer):
    def __init__(self, parent, paths, app):
        self.audio_list = paths
        self.current_episode = 0
        self.isfinished = False
        self.desktop_vol = 1.
        super().__init__(parent, app, True)
        
        self.finished_button = Button(self.bar,text='Apply Volume', command=self.save_destroy)
        self.finished_button.pack(side=LEFT)
        self.finished_all_button = Button(self.bar,text='Apply Volume to\nall episodes!', command=self.apply_vol_to_all_and_destroy)
        self.finished_all_button.pack(side=LEFT)
        
        self.desktop_volume_slider = Scale(
            self.controls, from_=0, to=100,
            orient=HORIZONTAL, label="Desktop Volume",
            command=self.set_volume_desktop
        )
        
        self.desktop_volume_slider.set(50)  # Set the default volume to 50%
        self.desktop_volume_slider.pack(side=LEFT, padx=5)
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


            self.open_file()
            self.play_video()
            self.current_media_label.configure(text=f'{self.current_media}')
            
    def episode_up(self,*args):
        """ Change the selected episode. One up. """
        new_location = self.current_episode + 1
        
        l = len(self.audio_list)
        
        if new_location > l - 1:
            self.current_episode = l - 1
        else:
            self.current_episode = new_location

            self.open_file()
            self.play_video()
            self.current_media_label.configure(text=f'{self.current_media}')
    def play_video(self):
        self.open_file()
        return super().play_video()
    
    def open_file(self):
        return super().open_file(self.media)
    
    def set_volume_desktop(self, value):
        self.desktop_vol = int(value)
        self.current_media[4] = self.desktop_vol / 100 if self.desktop_vol else 0
        
    def apply_vol_to_all_and_destroy(self):
        for media in self.audio_list:
            media[4] = self.desktop_vol
        self.save_destroy()
        
    def save_destroy(self):
        self.isfinished = True
        self.destroyed = True
        self.destroy()

        
  