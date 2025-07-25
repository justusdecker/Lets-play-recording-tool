from bin.automations_new import *
from bin.constants import DISCLAIMER
from bin.data_access import LetsPlay, Episode, on_start
from threading import Thread

import tkinter as tk
from tkinter import ttk

LARGEFONT =("Verdana", 35)

on_start()

class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        # initializing frames to an empty array
        self.frames = {}
        for F in (Main, Recording, ThumbnailGenerate, FetchAudio, FixAudio, Send2Audacity, CompAndRender, Settings):
 
            frame = F(container, self)
            
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(Main)
    def show_frame(self, cont):
        self.title(str(self.frames[cont]._name[1:]).capitalize())
        frame = self.frames[cont]
        frame.tkraise()

def get_menu(parent,controller) -> ttk.Frame:
    
    MENU = ttk.Frame(parent)
    
    OPTIONS = {'padx': 10, 'column': 0,'sticky':'W'}
    
    BUILDER: list[str, function] = [
        ("Main", lambda : controller.show_frame(Main)),
        ("Recording", lambda : controller.show_frame(Recording)),
        ("ThumbnailGenerate", lambda : controller.show_frame(ThumbnailGenerate)),
        ("FetchAudio", lambda : controller.show_frame(FetchAudio)),
        ("FixAudio", lambda : controller.show_frame(FixAudio)),
        ("Send2Audacity", lambda : controller.show_frame(Send2Audacity)),
        ("CompAndRender", lambda : controller.show_frame(CompAndRender)),
        ("Settings", lambda : controller.show_frame(Settings))
    ]
    
    _ret = [ttk.Button(MENU, text =obj[0], command = obj[1]) for obj in BUILDER]# create btns based on BUILDER
    
    [obj.grid(row = i, **OPTIONS) for i, obj in enumerate(_ret)]# Sets the position on frame for all btns
    
    MENU.grid(column=0,row=0)
    
    return _ret

def get_lets_play(parent,callback: callable) -> tuple[ttk.Label, ttk.OptionMenu,tk.StringVar, LetsPlay]:
    """
    Creates and configures Tkinter UI elements for selecting a "Let's Play" item.

    This function sets up a label and an option menu (dropdown) for users
    to select from a list of "Let's Play" names. The names are sourced
    from a `LetsPlay` object which conceptually reads from ROOT/'lets_plays.csv'.
    When a selection is made, the provided `callback` function is executed.
    """
    label = ttk.Label(parent, text ="Lets Play")

    label.grid(row = 0, column = 1) 
    
    lp_option_var = tk.StringVar(parent)
        
    lps = LetsPlay(LETS_PLAY_FILE_PATH)
    names = lps.get_names()
    options = ttk.OptionMenu(parent,lp_option_var,'None',*names,command=callback)
    
    options.grid(row = 0, column = 2)
    
    return label, options, lp_option_var, lps

def get_episode_range(parent, run_callback: callable, check_callback: callable,ft) -> tuple[ttk.Label, ttk.Label, ttk.Button, ttk.OptionMenu, ttk.OptionMenu, tk.StringVar, tk.StringVar]:
    """
    Creates and configures Tkinter UI elements for selecting an episode range.

    This function sets up two labels ("Episode start", "Episode end"),
    two option menus for selecting start and end episode numbers, and an
    "Extract" button. The button is initially disabled(if ft is none <- No data exists) and its state
    can be managed by the `check_callback`. The `run_callback` is
    executed when the "Extract" button is clicked.
    """
    label1 = ttk.Label(parent, text ="Episode start")

    label1.grid(row = 0, column = 3) 
    
    label2 = ttk.Label(parent, text ="Episode end")

    label2.grid(row = 0, column = 5) 

    start_btn = ttk.Button(parent, text ="Extract",command=run_callback)
    if not ft:
        start_btn.state(['disabled'])

    start_btn.grid(row = 0, column = 7) 
    
    epstart_option_var = tk.StringVar(parent)
    epend_option_var = tk.StringVar(parent)
    
    ep_start = ttk.OptionMenu(parent,epstart_option_var,str(ft[0] if ft else 'None'),*ft,command=check_callback)
    
    ep_start.grid(row = 0, column = 4) 
    
    ep_end = ttk.OptionMenu(parent,epend_option_var,str(ft[-1] if ft else 'None'),*ft,command=check_callback)
    
    ep_end.grid(row = 0, column = 6) 
    return label1, label2, start_btn, ep_start, ep_end, epstart_option_var, epend_option_var

def change_states(elements: list[ttk.Button],state: str):
    for element in elements:
        element.state([state])

class Main(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text =DISCLAIMER)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 
        
        VideoPlayer([1],Episode(ROOT + 'eps_test.csv'))
        
        get_menu(self, controller)
   
class VideoPlayer(Toplevel):
    def __init__(self, data: list[int],ep:Episode):
        self.data: list[int] = data
        self.episodes: Episode = ep
        self.current_episode = 0
        super().__init__()
        self.isfinished = False
        self.geometry('640x600')
        self.vol = 1.
        self.title_var = tk.StringVar()
        import vlc
        # Create a VLC instance and media player.
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        # Create the video panel where the video will be displayed.
        self.video_panel = tk.Frame(self, bg="black")
        self.video_panel.pack(fill=tk.BOTH, expand=1)
        
        self.open_file()
        
        self.bar = ttk.Frame(self)
        
        self.bar.pack(side=tk.LEFT, pady=5)
        # Set title each episode
        # Create a progress frame that holds the progress slider.
        self.progress_frame = tk.Frame(self)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create the progress slider.
        # This slider's range will be updated dynamically to match the video's duration.
        self.progress_slider = tk.Scale(
            self.progress_frame, from_=0, to=100,
            orient=tk.HORIZONTAL, showvalue=0, length=600
        )
        self.progress_slider.pack(fill=tk.X)
        self.progress_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_slider_release)
        self.slider_dragging = False

        # Create the control panel with playback buttons and volume control.
        self.controls = tk.Frame(self)
        self.controls.pack(fill=tk.X, padx=10, pady=5)

        # Last button.
        self.last_button = tk.Button(self.controls, text="Last", command=self.episode_down)
        self.last_button.pack(side=tk.LEFT, padx=5)

        # Next button.
        self.next_button = tk.Button(self.controls, text="Next", command=self.episode_up)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # Play button.
        self.play_button = tk.Button(self.controls, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT, padx=5)

        # Stop button.
        self.stop_button = tk.Button(self.controls, text="Stop", command=self.stop_video)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Volume control slider.
        # This slider controls the player's volume in real time.
        self.volume_slider = tk.Scale(
            self.controls, from_=0, to=100,
            orient=tk.HORIZONTAL, label="Volume",
            command=self.set_volume
        )
        self.volume_slider.set(50)  # Set the default volume to 50%
        self.volume_slider.pack(side=tk.LEFT, padx=5)

        self.label = ttk.Label(self.bar,text='Title: ')
        self.label.pack(side=tk.LEFT, padx=5)
        self.title_setter = ttk.Entry(self.bar,textvariable=self.title_var)
        self.title_setter.pack(side=tk.LEFT, padx=5)
        
        self.update_title_button = tk.Button(self.bar, text="Update", command=self.set_video_title)
        self.update_title_button.pack(side=tk.LEFT, padx=5)

        # Begin updating the progress slider periodically.
        self.update_progress()
    @property
    def rel_id(self) -> int:
        return self.data[self.current_episode] - 1
    @property
    def video_path(self) -> str:
        return self.episodes.get_final_video_path(self.rel_id)
    @property
    def video_title(self) -> str:
        return self.episodes.get_title(self.rel_id)
    @property
    def video_ep(self) -> str:
        return self.data[self.current_episode]
    def set_video_title(self,*args):
        self.episodes.set_title(self.rel_id, self.title_var.get())
        self.episodes.save()

    def episode_down(self,*args):

        new_location = self.current_episode - 1

        if new_location < 0:
            self.current_episode = 0
        else:
            self.current_episode = new_location

            self.title_setter.configure(text=f'{self.current_episode}')
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
            self.title_setter.configure(text=f'{self.current_episode}')
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
        self.episodes
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
            current_time = self.player.get_time()  # Current time in milliseconds.
            duration = self.player.get_length()      # Total duration in milliseconds.
            if duration > 0:
                self.progress_slider.config(to=duration)
                self.progress_slider.set(current_time)
        self.after(500, self.update_progress)
    

        
    def byebye(self, *args):
        """Closes the ThumbnailPreview window."""
        self.destroy()
class AutomationFrame(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.thread = None
        self.automation_callback = None
        
        self.pb = ttk.Progressbar(self)
        self.pb.grid(sticky='N',row = 0, column = 2)

        self.label, self.lp_options, self.lp_option_var, self.lps= get_lets_play(self, self.lp_changed)
        
        self.update_ui()
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self,self.run,self.check_last_id,self.epnums)
        
        self.menu = get_menu(self, controller)
    def update_ui(self):
        lp = self.lp_option_var.get()
        if lp != 'None':
            ep_path = self.lps.get_episode_path(self.lps.get_names().index(self.lp_option_var.get()))
            self.epnums = [i+1 for i in range(Episode(ROOT + ep_path).row)]
        else:
            self.epnums = []
    def run(self,*args):
        if self.thread is None:
            self.thread = Thread(target=self.__run)
            self.thread.start()
    def __run(self):
        self.start_btn.state(['disabled'])
        change_states(self.menu,'disabled')
        a, b = int(self.epstart_option_var.get()) , int(self.epend_option_var.get())
        lp = self.lps.get_names().index(self.lp_option_var.get())
        self.thread = self.automation_callback(lp,[a-1,b-1],self)
        
        change_states(self.menu,'!disabled')
        self.thread = None
    def lp_changed(self,*args):
        
        self.update_ui()
        
        if not self.epnums:
            self.start_btn.state(['disabled'])
        else:
            self.start_btn.state(['!disabled'])
        
        self.ep_start.destroy()
        self.ep_end.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.start_btn.destroy()
        del self.epstart_option_var
        del self.epend_option_var
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self,self.run,self.check_last_id,self.epnums)
        
    def check_last_id(self,*args):
        if int(self.epend_option_var.get()) < int(self.epstart_option_var.get()):
            self.start_btn.state(['disabled'])
        else:
            self.start_btn.state(['!disabled'])

class Recording(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.thread = None
        self.label1 = ttk.Label(self, text ="No Connection", font = LARGEFONT)

        self.label1.grid(row = 0, column = 3)
        
        self.btn_connect = ttk.Button(self, text ="Connect to obs",command=self.get_connection)

        self.btn_connect.grid(row = 0, column=4)
        
        self.label, self.lp_options, self.lp_option_var, self.lps= get_lets_play(self, self.lp_changed)
        self.btn_connect.state(["disabled"])
        
        #TODO
        #! Show selected Lets Play
        #! Show current Episode
        
        self.menu = get_menu(self, controller)
    def lp_changed(self,*args):
        print(self.lps.get_names().index(self.lp_option_var.get()))
        self.btn_connect.state(["!disabled"])
    def get_connection(self):
        self.lp_options.state(['disabled'])
        if self.thread is None:
            self.thread = Thread(target=self.__get_connection)
            self.thread.start()
    def __get_connection(self):
        
        change_states(self.menu,'disabled') # Deactivates all menu buttons for safety reasons
        ep = LetsPlay(LETS_PLAY_FILE_PATH).get_episodes(self.lps.get_names().index(self.lp_option_var.get()))
        self.btn_connect.state(["disabled"])
        self.btn_connect.configure(text='Try connection to OBS...')
        #! Currently Disconnecting only works by closing OBS <- mainly for safety reasons!
        obs_connect(ep,self)

        self.btn_connect.state(["!disabled"])
        change_states(self.menu,'!disabled') # Reactivating
        self.btn_connect.configure(text='Error occured! Try again')
        self.thread = None
        self.lp_options.state(['!disabled'])
            
class ThumbnailGenerate(AutomationFrame):
     def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.automation_callback = GenerateThumbnailWF
    
class FetchAudio(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.automation_callback = ExtractAudioWF
class FixAudio(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.automation_callback = FixAudioWF
class Send2Audacity(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.automation_callback = SendToAudacityWF

class CompAndRender(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.automation_callback = CompareAndRenderWF
    

class Settings(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="Nothing here currently", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        self.menu = get_menu(self, controller)
        

APP = TkinterApp()
APP.mainloop()


