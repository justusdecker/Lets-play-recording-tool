import tkinter.ttk as ttk
import tkinter as tk
from bin.constants import *
from bin.data_access import AsciiImage
from tkinter.messagebox import showerror
try:
    import vlc
except:
    showerror('ERROR', ERROR_008 + '\nvlc')
    quit()
VLC_INSTANCE = vlc.Instance()

class NewMediaPlayer(tk.Frame):
    """
    The Mediaplayer can play both video & audio.
    This class is a wrapper for `python-vlc`
    """
    
    def __init__(self,parent,app,audio_only: bool = False):
        self.app = app
        self.current_episode = 0
        super().__init__()
        self.isfinished = False

        
        self.instance = VLC_INSTANCE
        # Create a VLC instance and media player.
        self.player = self.instance.media_player_new()
        
        self.comp_panel = tk.Frame(parent)
        self.comp_panel.pack()
        
        # Create the video panel where the video will be displayed.
        self.video_panel = tk.Frame(self.comp_panel, bg="black")
        self.video_panel.pack(fill=tk.BOTH, expand=1)
        
        self.bar = tk.Frame(self.comp_panel)
        
        self.bar.pack(side=tk.LEFT, pady=5)
        # Set title each episode
        # Create a progress frame that holds the progress slider.
        self.progress_frame = tk.Frame(self.comp_panel)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create the progress slider.
        # This slider's range will be updated dynamically to match the video's duration.
        self.progress_value = tk.DoubleVar()
        self.progress_slider = tk.Scale(
            self.progress_frame, from_=0, to=100,
            orient=tk.HORIZONTAL, showvalue=0, length=600,variable=self.progress_value
        )
        self.progress_slider.pack(fill=tk.X)
        self.progress_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_slider_release)
        self.slider_dragging = False

        # Create the control panel with playback buttons and volume control.
        self.controls = ttk.Frame(self.comp_panel)
        self.controls.pack(fill=tk.X, padx=10, pady=5)

        # Last button.
        img = AsciiImage(ICO_BACKWARD)
        self.last_button = ttk.Button(self.controls, command=self.episode_down,image=img.image)
        self.last_button.pack(side=tk.LEFT, padx=5)
        self.last_button.image = img.image
        # Next button.
        img = AsciiImage(ICO_FORWARD)
        self.next_button = ttk.Button(self.controls, command=self.episode_up,image=img.image)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.next_button.image = img.image
        # Play button.
        img = AsciiImage(ICO_PLAY)
        self.play_button = ttk.Button(self.controls, command=self.play_video,image=img.image)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.play_button.image = img.image
        # Pause button.
        img = AsciiImage(ICO_PAUSE)
        self.pause_button = ttk.Button(self.controls, command=self.pause_video,image=img.image)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.image = img.image
        
        # Stop button
        img = AsciiImage(ICO_STOP)
        self.pause_button = ttk.Button(self.controls, command=self.stop_video,image=img.image)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.image = img.image
        
        # Volume control slider.
        # This slider controls the player's volume in real time.
        self.volume_slider = tk.Scale(
            self.controls, from_=0, to=100,
            orient=tk.HORIZONTAL, label="Volume",
            command=self.set_volume
        )
        
        self.volume_slider.set(50)  # Set the default volume to 50%
        self.volume_slider.pack(side=tk.LEFT, padx=5)

        # Begin updating the progress slider periodically.
        self.update_progress()
        
    def set_title(self):
        """ Set the window title """
        self.title(f'LPRT - MediaPlayer')
        
    def open_file(self, videopath: str):
        """
        Sets media to `video_path` in the VLC media player instance. Finally, it calls the method to embed
        the VLC video output into the Tkinter video panel.
        """
        if videopath:
            media = self.instance.media_new(videopath)
            self.player.set_media(media)
            self.set_video_panel()
            self.set_title()
            
    def episode_down(self,*args):
        pass
    
    def episode_up(self,*args):
        pass
    
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

            current_time = self.player.get_time()  # Current time in milliseconds.
            duration = self.player.get_length()      # Total duration in milliseconds.
            if duration > 0:
                self.progress_slider.config(to=duration)
                self.progress_slider.set(current_time)

        self.after(500, self.update_progress)
    
    def destroy(self):
        self.stop_video()
        return super().destroy()


class MediaPlayer(tk.Toplevel):
    """
    The Mediaplayer can play both video & audio.
    This class is a wrapper for `python-vlc`
    """
    
    def __init__(self,app,audio_only: bool = False):
        self.app = app
        self.current_episode = 0
        super().__init__()
        self.isfinished = False
        if audio_only:
            self.geometry('640x300')
        else:
            self.geometry('640x600')

        
        self.instance = VLC_INSTANCE
        # Create a VLC instance and media player.
        self.player = self.instance.media_player_new()
        
        # Create the video panel where the video will be displayed.
        self.video_panel = tk.Frame(self, bg="black")
        self.video_panel.pack(fill=tk.BOTH, expand=1)
        
        self.bar = tk.Frame(self)
        
        self.bar.pack(side=tk.LEFT, pady=5)
        # Set title each episode
        # Create a progress frame that holds the progress slider.
        self.progress_frame = tk.Frame(self)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create the progress slider.
        # This slider's range will be updated dynamically to match the video's duration.
        self.progress_value = tk.DoubleVar()
        self.progress_slider = tk.Scale(
            self.progress_frame, from_=0, to=100,
            orient=tk.HORIZONTAL, showvalue=0, length=600,variable=self.progress_value
        )
        self.progress_slider.pack(fill=tk.X)
        self.progress_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_slider_release)
        self.slider_dragging = False

        # Create the control panel with playback buttons and volume control.
        self.controls = ttk.Frame(self)
        self.controls.pack(fill=tk.X, padx=10, pady=5)

        # Last button.
        img = AsciiImage(ICO_BACKWARD)
        self.last_button = ttk.Button(self.controls, command=self.episode_down,image=img.image)
        self.last_button.pack(side=tk.LEFT, padx=5)
        self.last_button.image = img.image
        # Next button.
        img = AsciiImage(ICO_FORWARD)
        self.next_button = ttk.Button(self.controls, command=self.episode_up,image=img.image)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.next_button.image = img.image
        # Play button.
        img = AsciiImage(ICO_PLAY)
        self.play_button = ttk.Button(self.controls, command=self.play_video,image=img.image)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.play_button.image = img.image
        # Pause button.
        img = AsciiImage(ICO_PAUSE)
        self.pause_button = ttk.Button(self.controls, command=self.pause_video,image=img.image)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.image = img.image
        
        # Stop button
        img = AsciiImage(ICO_STOP)
        self.pause_button = ttk.Button(self.controls, command=self.stop_video,image=img.image)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.image = img.image
        
        # Volume control slider.
        # This slider controls the player's volume in real time.
        self.volume_slider = tk.Scale(
            self.controls, from_=0, to=100,
            orient=tk.HORIZONTAL, label="Volume",
            command=self.set_volume
        )
        
        self.volume_slider.set(50)  # Set the default volume to 50%
        self.volume_slider.pack(side=tk.LEFT, padx=5)

        # Begin updating the progress slider periodically.
        self.update_progress()
        
    def set_title(self):
        """ Set the window title """
        self.title(f'LPRT - MediaPlayer')
        
    def open_file(self, videopath: str):
        """
        Sets media to `video_path` in the VLC media player instance. Finally, it calls the method to embed
        the VLC video output into the Tkinter video panel.
        """
        if videopath:
            media = self.instance.media_new(videopath)
            self.player.set_media(media)
            self.set_video_panel()
            self.set_title()
            
    def episode_down(self,*args):
        pass
    
    def episode_up(self,*args):
        pass
    
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

            current_time = self.player.get_time()  # Current time in milliseconds.
            duration = self.player.get_length()      # Total duration in milliseconds.
            if duration > 0:
                self.progress_slider.config(to=duration)
                self.progress_slider.set(current_time)

        self.after(500, self.update_progress)
    
    def destroy(self):
        self.stop_video()
        return super().destroy()
