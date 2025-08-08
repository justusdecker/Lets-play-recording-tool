import tkinter.ttk as ttk
from tkinter import (
    Toplevel,
    StringVar,
    BOTH,
    LEFT,
    HORIZONTAL,
    X
)
import tkinter as tk

from tkinter.messagebox import showerror

try:
    import vlc
except:
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nvlc')
    quit()

from bin.data_access import SQLAccess
from bin.thumbnail import ThumbnailGenerator
from bin.constants import *
from bin.ffmpeg import *

CHAR_TABLE = {
        'Ä':'&Auml;',
        'Ö':'&Ouml;',
        'Ü':'&Uuml;',
        'ä':'&auml;',
        'ö':'&ouml;',
        'ü':'&uuml;',
        'ß':'&szlig;'
     }

def convert_char(c: str):
    if not c in CHAR_TABLE: return c
    return CHAR_TABLE[c]


class VideoPlayer(Toplevel):
    def __init__(self, data: list[int],lpid,app):
        self.tg = ThumbnailGenerator()
        self.app = app
        self.data: list[int] = data
        self.current_episode = 0
        super().__init__()
        self.isfinished = False
        self.geometry('640x600')
        self.vol = 1.
        self.title_var = StringVar()
        self.lpid = lpid
        # Create a VLC instance and media player.
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        # Create the video panel where the video will be displayed.
        self.video_panel = tk.Frame(self, bg="black")
        self.video_panel.pack(fill=BOTH, expand=1)
        
        self.open_file()
        
        self.bar = ttk.Frame(self)
        
        self.bar.pack(side=LEFT, pady=5)
        # Set title each episode
        # Create a progress frame that holds the progress slider.
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(fill=X, padx=10, pady=5)
        
        # Create the progress slider.
        # This slider's range will be updated dynamically to match the video's duration.
        self.progress_value = tk.DoubleVar()
        self.progress_slider = tk.Scale(
            self.progress_frame, from_=0, to=100,
            orient=HORIZONTAL, showvalue=0, length=600,variable=self.progress_value
        )
        self.progress_slider.pack(fill=X)
        self.progress_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_slider_release)
        self.slider_dragging = False

        # Create the control panel with playback buttons and volume control.
        self.controls = ttk.Frame(self)
        self.controls.pack(fill=X, padx=10, pady=5)

        # Last button.
        self.last_button = ttk.Button(self.controls, text="Last", command=self.episode_down)
        self.last_button.pack(side=LEFT, padx=5)

        # Next button.
        self.next_button = ttk.Button(self.controls, text="Next", command=self.episode_up)
        self.next_button.pack(side=LEFT, padx=5)
        
        # Play button.
        self.play_button = ttk.Button(self.controls, text="Play", command=self.play_video)
        self.play_button.pack(side=LEFT, padx=5)

        # Stop button.
        self.stop_button = ttk.Button(self.controls, text="Pause", command=self.pause_video)
        self.stop_button.pack(side=LEFT, padx=5)

        # Volume control slider.
        # This slider controls the player's volume in real time.
        self.volume_slider = tk.Scale(
            self.controls, from_=0, to=100,
            orient=HORIZONTAL, label="Volume",
            command=self.set_volume
        )
        self.volume_slider.set(50)  # Set the default volume to 50%
        self.volume_slider.pack(side=LEFT, padx=5)

        ttk.Label(self.bar,text='Title: ').pack(side=LEFT, padx=5)
        self.title_setter = ttk.Entry(self.bar,textvariable=self.title_var)
        self.title_setter.pack(side=LEFT, padx=5)
        
        
        
        self.update_title_button = ttk.Button(self.bar, text="Update", command=self.set_video_title)
        self.update_title_button.pack(side=LEFT, padx=5)
        
        self.take_thumbnail_btn = ttk.Button(self.bar,text='Generate Thumbnail',command=self.gen_thumbnail)
        self.take_thumbnail_btn.pack(side=LEFT, padx=5)

        # Begin updating the progress slider periodically.
        self.update_progress()
        self.blocked = False
    def gen_thumbnail(self,*args):
        if self.blocked: return
        self.blocked = True
        length = ffmpeg_run(FFMPEG_GET_LENGTH)
        if length is None: return
        frame = self.progress_value.get() * length
        self.stop_video()

        self.tg.generate(
            str(self.current_episode),
            self.video_path,
            SQLAccess.get_tad_path(self.lpid),
            f'{THUMBNAIL_FOLDER}_generated_from_video_{self.current_episode}.png',
            frame
            )
        self.open_file()
        print('finished generating')
        self.blocked = False
    @property
    def rel_id(self) -> int:
        return self.data[self.current_episode] - 1
    @property
    def video_path(self) -> str:
        return SQLAccess.get_final_video_path(self.lpid,self.rel_id)
    @property
    def video_title(self) -> str:
        return SQLAccess.get_title(self.lpid,self.rel_id)
    @property
    def video_ep(self) -> str:
        return self.data[self.current_episode]
    def set_video_title(self,*args):
        new_title = ''.join([convert_char(c) for c in self.title_var.get()])
        SQLAccess.update_episodes(self.lpid, self.rel_id,title=new_title)

    def episode_down(self,*args):

        new_location = self.current_episode - 1

        if new_location < 0:
            self.current_episode = 0
        else:
            self.current_episode = new_location

            self.title_var.set(f'{self.video_title}')
            self.set_title()
            self.open_file()
            self.play_video()
    def episode_up(self,*args):

        new_location = self.current_episode + 1
        
        l = len(self.data)
        
        if new_location > l - 1:
            self.current_episode = l - 1
            

        else:
            self.current_episode = new_location
            self.title_var.set(f'{self.video_title}')
            self.set_title()
            self.open_file()
            self.play_video()
    def open_file(self):
        """
        This function opens a file dialog for the user to select a video file.
        It then creates a new VLC media object from the selected file and sets it
        to the VLC media player instance. Finally, it calls the method to embed
        the VLC video output into the Tkinter video panel.
        """
        if self.video_path:
            media = self.instance.media_new(self.video_path)
            self.player.set_media(media)
            self.set_video_panel()
            self.title_var.set(f'{self.video_title}')
            self.set_title()
    def set_title(self):
        self.title(f'[{self.video_ep}]{self.video_path} - [{self.current_episode}]')
    def set_video_panel(self):
        """
        This function embeds the VLC player's video output into the Tkinter video panel.
        It retrieves the window ID of the video panel and then assigns it to the VLC media player
        using platform-specific method: set_hwnd.
        """
        self.player.set_hwnd(self.video_panel.winfo_id())
    def play_video(self):
        """
        Once the media is loaded via the open_file function, clicking the Play button 
        will trigger this function to begin playback.
        """
        self.player.play()

    def pause_video(self):#! Not in use
        """
        The pause_video function toggles the current playback state. If the video is playing,
        it pauses the playback; if it's paused, it resumes playing. 
        """
        self.player.pause()

    def stop_video(self):
        """
        The stop_video function stops the video playback completely and resets the playback state.
        """
        self.player.stop()

    def set_volume(self, value):
        """
        Adjusts the player's volume.
        This function is triggered whenever the volume slider is moved.
        """
        self.vol = int(value)
        self.player.audio_set_volume(self.vol)

    def on_slider_press(self, event):
        """
        Triggered when the user begins dragging the progress slider.
        This sets a flag indicating manual adjustment is in progress,
        preventing automatic updates from interfering.
        """
        self.slider_dragging = True

    def on_slider_release(self, event):
        """
        Triggered when the user releases the progress slider.
        It resets the dragging flag and seeks the video to the slider's position.
        """
        self.slider_dragging = False
        self.seek_video()

    def seek_video(self):
        """
        Seeks the video to a new position based on the slider's value.
        The slider's value represents the time in milliseconds.
        """
        slider_value = self.progress_slider.get()
        self.player.set_time(int(slider_value))

    def update_progress(self):
        """
        Updates the progress slider to reflect the current playback time.
        If the slider is not being manually adjusted by the user,
        this function retrieves the current playback time and the video's total length,
        updates the slider's range if necessary, and sets the slider to the current time.
        This function is called repeatedly every 500 milliseconds.
        """
        if not self.slider_dragging:
            try:
                current_time = self.player.get_time()  # Current time in milliseconds.
                duration = self.player.get_length()      # Total duration in milliseconds.
                if duration > 0:
                    self.progress_slider.config(to=duration)
                    self.progress_slider.set(current_time)
            except:
                pass
        self.after(500, self.update_progress)
    
    def destroy(self):
        self.app.start_btn.state(['!disabled'])
        for element in self.app.menu:

            element.state(['!disabled'])
        for element in [self.app.label, self.app.lp_options,self.app.label2, self.app.label3,self.app.ep_end, self.app.ep_start]:
            element.state(['!disabled'])
        return super().destroy()
