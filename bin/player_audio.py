from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

from tkinter import Toplevel, DoubleVar
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

def play_audio(filepath: str):
    """
    Loads and plays an audio file indefinitely.

    This function first stops any currently playing audio, then loads the
    specified audio file and plays it in a continuous loop.

    Args:
        filepath (str): The path to the audio file to be played.
    """
    stop_audio()
    music.load(filepath)
    music.play(loops=-1)

def stop_audio():
    """
    Stops the currently playing audio.

    If audio is currently playing, this function stops it and unloads the
    audio file from memory.
    """
    if music.get_busy():
        music.stop()
        music.unload()





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
        self.audio_list[self.current_episode][4] = self.get_volume()
        stop_audio()
        ffmpeg_run(FFMPEG_AUDIO_COMBINE_TRUNCATED,{'__IN1__':self.audio_list[self.current_episode][1],'__IN2__': self.audio_list[self.current_episode][2],'__VOLUME1__': str(1.0),'__VOLUME2__': str(self.audio_list[self.current_episode][4]),'__OUT__':f'{TEMP_FOLDER}temp.mp3'})
        play_audio(f'{TEMP_FOLDER}temp.mp3')
        
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
     