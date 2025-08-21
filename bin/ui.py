from tkinter import ttk
import tkinter as tk
from tkinter.font import Font
from bin.constants import *
from bin.constants import __LICENSE__
from bin.data_access import SQLAccess, AsciiImage, json_write, json_read, try_delete_file
from threading import Thread
from bin.welcome_popup import WELCOME
from bin.automations import *
from os.path import getsize
from zipfile import ZipFile
import sys
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from bin.player_video import NewVideoPlayer
from bin.player_audio import NewAudioPlayer
from bin.gemini_api import send_gemini



def get_lets_play(parent,callback: callable) -> tuple[ttk.Label, ttk.OptionMenu,tk.StringVar]:
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
        
    #lps = LetsPlays
    names = SQLAccess.read_letsplay_names()
    options = ttk.OptionMenu(parent,lp_option_var,'None',*names,command=callback)
    
    options.grid(row = 0, column = 2)
    
    return label, options, lp_option_var

def get_episode_range(parent, run_callback: callable, check_callback: callable,ft) -> tuple[ttk.Label, ttk.Label, ttk.Button, ttk.OptionMenu, ttk.OptionMenu, tk.StringVar, tk.StringVar]:
    """
    Creates and configures Tkinter UI elements for selecting an episode range.

    This function sets up two lab els ("Episode start", "Episode end"),
    two option menus for selecting start and end episode numbers, and an
    "Run" button. The button is initially disabled(if ft is none <- No data exists) and its state
    can be managed by the `check_callback`. The `run_callback` is
    executed when the "Run" button is clicked.
    """
    label1 = ttk.Label(parent, text ="Episode start")

    label1.grid(row = 0, column = 3) 
    
    label2 = ttk.Label(parent, text ="Episode end")

    label2.grid(row = 0, column = 5) 
    img = AsciiImage(ICO_RUN)
    
    start_btn = ttk.Button(parent, image=img.image,command=run_callback)
    start_btn.image = img.image
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
    """
    Changes the state of a list of Tkinter `ttk.Button` widgets.

    This function iterates through a given list of `ttk.Button` objects
    and applies a specified state to each one. This can be used to enable,
    disable, or otherwise alter the visual and interactive state of buttons.
    """
    for element in elements:

        element.state([state])

class Notebook:
    def __init__(self, 
                 parent: tk.Tk | tk.Widget,
                 ui: list[str]):
        self.parent = parent
        
        self.notebook = ttk.Notebook(self.parent)
        
        self.frames = []
        self.names = ui.copy()
        
        for i in range(len(ui)):
            
            f = ttk.Frame(self.notebook)
            f.pack(padx=5,pady=5)
            self.notebook.add(f,text=self.names[i])
            self.frames.append(f)
        self.notebook.pack(padx=5,pady=5)
            
    def get_root_for(self,name: str):
        if not name in self.names: raise NameError
        return self.frames[self.names.index(name)]
                   
class TkinterApp(tk.Tk):
    """
    The main application window for the multi-page Tkinter application.

    This class extends `tk.Tk` and provides a framework for managing
    multiple distinct pages (frames) within a single window. It initializes
    each page and allows seamless navigation between them.
    """
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        
        
        self.menu = Notebook(self,self.get_ui_names())
        self.title(f'LPRT - {VERSION}:{HASH}')
        self.geometry('1024x768')
        self.build_ui()
        WELCOME.destroy()
        
        AI = AsciiImage(IMG_LOGO)
    
        self.wm_iconphoto(False,AI.image)
    def get_ui_names(self) -> list[str]:
        return [
            'Main',
            'Recording',
            'ThumbnailGenerate',
            'FetchAudio',
            'FixAudio',
            'Send2Audacity',
            'Deploy',
            'FileManager',
            'TadEditor',
            'CompAndRender',
            'SetTitle',
            'Settings',
            'About',
        ]
    def build_ui(self):
        ELEMENTS = [
            (Main, 'Main'),
            (Recording, 'Recording'),
            (ThumbnailGenerate,'ThumbnailGenerate'),
            (FetchAudio,'FetchAudio'),
            (FixAudio,'FixAudio'),
            (Send2Audacity,'Send2Audacity'),
            (CompAndRender,'CompAndRender'),
            (SetTitle,'SetTitle'),
            (Deploy,'Deploy'),
            (TadEditor,'TadEditor'),
            (FileManager,'FileManager'),
            (Settings,'Settings'),
            (About, 'About')
        ]
        for ui,name in ELEMENTS:
            ui(self.menu.get_root_for(name))

class Main(tk.Frame):
    """
    Represents the main start page of the application.

    This frame serves as the initial view for the application,
    displaying a welcome message and a disclaimer, and integrating the
    navigation menu for other application pages.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        
        # Create Headers
        MAIN = ttk.LabelFrame(W,text='Welcome')
        
        label = ttk.Label(MAIN, text =DISCLAIMER)

        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Packing
        MAIN.pack()

        W.pack()
       
class Recording(tk.Frame):
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        self.thread = None
        W = ttk.Frame(parent)
        
        self.menu = parent.master
        
        # Create Headers
        RECORDING = ttk.LabelFrame(W,text='Recording')
        
        INFORMATION = ttk.LabelFrame(W,text='Information')

        
        # Recording
        self.btn_connect = ttk.Button(RECORDING, text ="Connect to obs",command=self.get_connection)

        self.btn_connect.grid(row = 0, column=4)
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(RECORDING, self.lp_changed)
        
        # Information
        self.recording_information_label = ttk.Label(INFORMATION, text ="No Connection",font=Font(W,size=12))

        self.recording_information_label.grid(row = 0, column = 1)
        
        # Packing
        RECORDING.pack()
        INFORMATION.pack()
        
        W.grid(row=0,column=1)

        # Disable connect button
        self.btn_connect.state(["disabled"])
        
    def lp_changed(self,*args):
        self.btn_connect.state(["!disabled"])
    def get_connection(self):
        if self.thread:
            self.close_connection = True
        self.lp_options.state(['disabled'])
        if self.thread is None:
            self.close_connection = False
            self.thread = Thread(target=self.__get_connection)
            self.thread.start()
    def __get_connection(self):
        
        change_states([self.menu],'disabled') # Deactivates all menu buttons for safety reasons
        
        ep = SQLAccess.read_episodes(SQLAccess.read_letsplay_names().index(self.lp_option_var.get()))
        self.btn_connect.state(["disabled"])
        self.btn_connect.configure(text='Try connection to OBS...')
        #! Currently Disconnecting only works by closing OBS <- mainly for safety reasons!
        obs_connect(self)

        self.btn_connect.state(["!disabled"])
        change_states([self.menu],'!disabled') # Reactivating
        if not self.close_connection:
            self.btn_connect.configure(text='Error occured! Try again')
        self.thread = None
        self.lp_options.state(['!disabled'])

     
class TKFrameWithLPControls(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.menu = parent.master
        
        W = tk.Frame(parent)
        
        AUTOMATION_ROOT = ttk.Frame(W)
        
        self.normal_options = ttk.LabelFrame(AUTOMATION_ROOT,text=f'LP & EP Selection')

        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(self.normal_options, self.lp_changed)
        
        self.update_ui()
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.normal_options,self.run,self.check_last_id,self.epnums)
        
        self.normal_options.pack()
        AUTOMATION_ROOT.pack()
        W.pack()
        self.W = W
    
    def update_ui(self):
        """
        Updates the UI elements based on the selected 'Let's Play' series.

        This method dynamically calculates the available episode numbers
        based on the currently selected 'Let's Play' value and updates
        the internal `epnums` list.
        """
        lp = self.lp_option_var.get()
        if lp != 'None':
            self.epnums = [i+1 for i in range(SQLAccess.read_episode_ammount(SQLAccess.read_letsplay_by_option_var(self)))]
        else:
            self.epnums = []
    
    def lp_changed(self,*args):
        """
        Callback function executed when the 'Let's Play' selection changes.

        This method updates the UI based on the new 'Let's Play' selection,
        recalculates available episode numbers, and dynamically rebuilds
        the episode range selection widgets. It also adjusts the state
        of the start button.
        """
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
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.normal_options,self.run,self.check_last_id,self.epnums)
        
    def check_last_id(self,*args):
        """
        Validates the selected episode range.

        This callback is triggered when either the start or end episode
        selection changes. It disables the start button if the end episode
        is numerically less than the start episode, ensuring valid range selection.
        """
        if int(self.epend_option_var.get()) < int(self.epstart_option_var.get()):
            self.start_btn.state(['disabled'])
        else:
            self.start_btn.state(['!disabled'])
         
class ThumbnailGenerate(TKFrameWithLPControls):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.check_for_each_option_var = tk.BooleanVar(value=False)
        
        options = ttk.LabelFrame(self.W,text='Options')
        
        
        self.check_for_each_option = ttk.Checkbutton(options, text='Check each', variable=self.check_for_each_option_var)
        self.check_for_each_option.pack()
        
        preview = ttk.LabelFrame(self.W,text='Preview')
        
        self.tp = ThumbnailPreview(preview)
        self.tp.pack()
        options.pack()
        preview.pack()
        self.thread = None
        
        #- Image Canvas to render on <- comes after refactoring player_thumbnail
        
    def run(self):
        if self.thread is None:
            self.thread = Thread(target=self.__run)
            self.thread.start()
        
    def __run(self):
        print(f'run automation with cfe set as [{self.check_for_each_option_var.get()}]. In range: [{self.epstart_option_var.get()} - {self.epend_option_var.get()}]')

        self.start_btn.state(['disabled'])
        change_states([self.menu],'disabled')
        change_states([self.label, self.lp_options],'disabled')
        change_states([self.label2, self.label3,self.ep_end, self.ep_start],'disabled')
        a, b = int(self.epstart_option_var.get()) , int(self.epend_option_var.get())
        
        lp = SQLAccess.read_letsplay_by_option_var(self)
        
        GenerateThumbnailWF(lp,[a-1,b],self)
        
        change_states([self.menu],'!disabled')
        change_states([self.label, self.lp_options],'!disabled')
        change_states([self.label2, self.label3,self.ep_end, self.ep_start],'!disabled')
        self.thread = None
    

class AutomationFrame(tk.Frame):
    """
    A base class for frames that perform automated tasks, such as thumbnail generation
    or audio processing.

    This frame provides common UI elements and logic for managing automation
    processes, including a progress bar, a navigation menu, and controls for
    selecting "Let's Play" series and episode ranges. It supports running
    automation tasks in a separate thread to keep the UI responsive.
    
    
    Attributes:
        should_not_reset (bool): If True, the UI elements will not be re-enabled
                                 after the automation thread completes.
        thread (threading.Thread or None): The background thread running the automation task.
        automation_callback (callable or None): A function that will be called to start
                                                 the actual automation process.
        progress_label (ttk.Label): A label to display progress updates.
        menu (list[ttk.Button]): The navigation menu buttons.
        THUMBNAIL_AUTOMATION (ttk.Frame): A sub-frame for automation-specific controls.
        label (ttk.Label): Label for 'Let's Play' selection.
        lp_options (ttk.OptionMenu): Dropdown for 'Let's Play' selection.
        lp_option_var (tk.StringVar): Tkinter variable holding the selected 'Let's Play' value.
        epnums (list[int]): List of available episode numbers for the selected 'Let's Play'.
        label2 (ttk.Label): Label for start episode selection.
        label3 (ttk.Label): Label for end episode selection.
        start_btn (ttk.Button): Button to start the automation.
        ep_start (ttk.OptionMenu): Dropdown for start episode selection.
        ep_end (ttk.OptionMenu): Dropdown for end episode selection.
        epstart_option_var (tk.StringVar): Tkinter variable holding the selected start episode.
        epend_option_var (tk.StringVar): Tkinter variable holding the selected end episode.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        self.menu = parent.master
        self.should_not_reset = False
        self.thread = None
        self.automation_callback = None
        
        self.progress_label = ttk.Label(self,)
        self.progress_label.grid(sticky='SE',row = 0, column = 2)
        
        W = ttk.Frame(parent)
        
        # Create Headers
        AUTOMATION_ROOT = ttk.Frame(W)
        
        self.normal_options = ttk.LabelFrame(AUTOMATION_ROOT,text=f'LP & EP Selection')

        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(self.normal_options, self.lp_changed)
        
        
        self.update_ui()
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.normal_options,self.run,self.check_last_id,self.epnums)
        
        self.normal_options.pack()

        AUTOMATION_ROOT.pack()
        
        W.pack()
        
    def update_ui(self):
        """
        Updates the UI elements based on the selected 'Let's Play' series.

        This method dynamically calculates the available episode numbers
        based on the currently selected 'Let's Play' value and updates
        the internal `epnums` list.
        """
        lp = self.lp_option_var.get()
        if lp != 'None':
            self.epnums = [i+1 for i in range(SQLAccess.read_episode_ammount(SQLAccess.read_letsplay_by_option_var(self)))]
        else:
            self.epnums = []
            
    def run(self,*args):
        """
        Initiates the automation process in a separate thread.

        This method checks if an automation thread is already running.
        If not, it creates a new thread to execute the `__run` method
        and starts it, preventing the UI from freezing.
        """
        if self.thread is None:
            self.thread = Thread(target=self.__run)
            self.thread.start()
            
    def __run(self):
        """
        The core automation execution method, run in a separate thread.

        This private method disables relevant UI elements, executes the
        `automation_callback` with the selected parameters, and then
        re-enables the UI elements upon completion unless `should_not_reset` is True.
        """
        self.start_btn.state(['disabled'])
        change_states([self.menu],'disabled')
        change_states([self.label, self.lp_options],'disabled')
        change_states([self.label2, self.label3,self.ep_end, self.ep_start],'disabled')
        a, b = int(self.epstart_option_var.get()) , int(self.epend_option_var.get())
        
        lp = SQLAccess.read_letsplay_by_option_var(self)
        self.automation_callback(lp,[a-1,b],self)
        
        if not self.should_not_reset:
            
            change_states([self.menu],'!disabled')
            change_states([self.label, self.lp_options],'!disabled')
            change_states([self.label2, self.label3,self.ep_end, self.ep_start],'!disabled')

        self.thread = None
        
    def lp_changed(self,*args):
        """
        Callback function executed when the 'Let's Play' selection changes.

        This method updates the UI based on the new 'Let's Play' selection,
        recalculates available episode numbers, and dynamically rebuilds
        the episode range selection widgets. It also adjusts the state
        of the start button.
        """
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
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.normal_options,self.run,self.check_last_id,self.epnums)
        
    def check_last_id(self,*args):
        """
        Validates the selected episode range.

        This callback is triggered when either the start or end episode
        selection changes. It disables the start button if the end episode
        is numerically less than the start episode, ensuring valid range selection.
        """
        if int(self.epend_option_var.get()) < int(self.epstart_option_var.get()):
            self.start_btn.state(['disabled'])
        else:
            self.start_btn.state(['!disabled'])

class FetchAudio(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = ExtractAudioWF

class FixAudio(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = FixAudioWF
        audio_filters_frame = ttk.Frame(self.AUTOMATION_ROOT)
        audio_filters_frame.pack(pady=10,)

        # Highpass Filter
        hp_frame = ttk.LabelFrame(audio_filters_frame, text="High-Pass Filter")
        hp_frame.pack(fill='x', padx=5, pady=5)
        
        self.hp_enabled = tk.BooleanVar(value=False)
        self.hp_freq = tk.DoubleVar(value=175.0)
        
        ttk.Checkbutton(hp_frame, text="Aktivate", variable=self.hp_enabled).grid(row=0, column=0, sticky='w')
        ttk.Label(hp_frame, text="Frequency (Hz):").grid(row=0, column=1, sticky='w')
        ttk.Spinbox(
            hp_frame,
            from_=20.0,
            to=5000.0,
            increment=1.0,
            textvariable=self.hp_freq,
            width=8
        ).grid(row=0, column=2, sticky='w')

        # Lowpass Filter
        lp_frame = ttk.LabelFrame(audio_filters_frame, text="Low-Pass Filter")
        lp_frame.pack(fill='x', padx=5, pady=5)
        
        self.lp_enabled = tk.BooleanVar(value=False)
        self.lp_freq = tk.DoubleVar(value=13000.0)
        
        ttk.Checkbutton(lp_frame, text="Aktivate", variable=self.lp_enabled).grid(row=0, column=0, sticky='w')
        ttk.Label(lp_frame, text="Frequency (Hz):").grid(row=0, column=1, sticky='w')
        ttk.Spinbox(
            lp_frame,
            from_=500.0,
            to=20000.0,
            increment=100.0,
            textvariable=self.lp_freq,
            width=8
        ).grid(row=0, column=2, sticky='w')

        # Loudness Normalization
        ln_frame = ttk.LabelFrame(audio_filters_frame, text="Loudness Normalization")
        ln_frame.pack(fill='x', padx=5, pady=5)
        
        self.ln_enabled = tk.BooleanVar(value=True)
        self.ln_i = tk.DoubleVar(value=-15.0)
        self.ln_tp = tk.DoubleVar(value=-1.5)
        self.ln_lra = tk.DoubleVar(value=11.0)
        
        ttk.Checkbutton(ln_frame, text="Aktivate", variable=self.ln_enabled).grid(row=0, column=0, sticky='w', columnspan=2)
        
        ttk.Label(ln_frame, text="Integrated (LUFS):").grid(row=1, column=0, sticky='w')
        ttk.Spinbox(
            ln_frame,
            from_=-24.0,
            to=-10.0,
            increment=0.5,
            textvariable=self.ln_i,
            width=6
        ).grid(row=1, column=1, sticky='w')

        ttk.Label(ln_frame, text="True Peak (dBTP):").grid(row=2, column=0, sticky='w')
        ttk.Spinbox(
            ln_frame,
            from_=-6.0,
            to=0.0,
            increment=0.1,
            textvariable=self.ln_tp,
            width=6
        ).grid(row=2, column=1, sticky='w')

        ttk.Label(ln_frame, text="Loudness Range (LU):").grid(row=3, column=0, sticky='w')
        ttk.Spinbox(
            ln_frame,
            from_=1.0,
            to=20.0,
            increment=1.0,
            textvariable=self.ln_lra,
            width=6
        ).grid(row=3, column=1, sticky='w')

    def get_ffmpeg_audio_filter_string(self):
        """
        Constructs the FFmpeg audio filter string based on the current UI settings.
        Returns the filter string or None if no filters are enabled.
        """
        filters = []
        
        # Highpass Filter
        if self.hp_enabled.get():
            filters.append(f"highpass=f={self.hp_freq.get()}")
            
        # Lowpass Filter
        if self.lp_enabled.get():
            filters.append(f"lowpass=f={self.lp_freq.get()}")

        # Loudness Normalization
        if self.ln_enabled.get():
            filters.append(f"loudnorm=I={self.ln_i.get()}:TP={self.ln_tp.get()}:LRA={self.ln_lra.get()}")
        
        if not filters: # This will prevent no audio filter usage!
            raise AutomationError
        
        return ", ".join(filters)

class Send2Audacity(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = SendToAudacityWF
        
class Deploy(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = DeployWF
       

class FileManager(tk.Frame):
    """
    Manages file-related operations within the application, including:
    - Detecting file sizes and counts for various data categories.
    - Providing options for deleting episode-specific and 'Let's Play' specific files.
    - Functionality to create new 'Let's Play' entries.
    - Options to backup 'Let's Play' related video and TAD files into a ZIP archive.
    
    This frame serves as a central hub for data management and maintenance.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        # Menu
        self.menu = parent.master
        # Data Detection
        open_folder_btn = ttk.Button(W,text='Open lprt folder',command=lambda *x: Popen(f'explorer {ROOT}'))
        open_folder_btn.pack()
        DATA_DETECTION = ttk.LabelFrame(W,text='Data Detection')
        
        self.detect_btn = ttk.Button(DATA_DETECTION, text='Detect',command=self.on_detect)
        self.label = ttk.Label(DATA_DETECTION,text='')
        
        self.detect_btn.grid(row=0,column=0)
        self.label.grid(row=0,column=1)
        DATA_DETECTION.pack()
        

        
        
        
        # Data Deletion
        
        DATA_DELETION = ttk.LabelFrame(W,text='Data Deletion')
        self.DATA_DELETION = DATA_DELETION
        
        self.simdel_lp_label, self.simdel_lp_options, self.simdel_lp_option_var= get_lets_play(DATA_DELETION, self.lp_changed)
        
        self.simdel_label2, self.simdel_label3, self.start_btn, self.simdel_ep_start, self.simdel_ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(DATA_DELETION,lambda x: None,self.check_last_id,[])
        self.start_btn.destroy()
        
        self.delete_btn = ttk.Button(DATA_DELETION, text='Delete',command=self.delete_files)
        self.delete_btn.state(['disabled'])
        
        self.delete_btn.grid(row=0,column=7,pady=5)
        
        DATA_DELETION.pack()
        
        
        # Lets Play Delete
        LP_DELETE = ttk.LabelFrame(W,text='Lets Play Delete')
        
        self.delete_lp_option = tk.IntVar(value=0)
        
        self.lp_label, self.lp_options, self.lp_option_var= get_lets_play(LP_DELETE, self.something_changed_delete)
        self.btn_lp_delete = ttk.Button(LP_DELETE,text='Delete',command=self.delete_lets_play)
        self.btn_lp_delete.state(['disabled'])
        self.delete_files_del_lp = ttk.Checkbutton(LP_DELETE,text='Delete Files?',variable=self.delete_lp_option, onvalue=1, offvalue=0)
        
        self.delete_files_del_lp.grid(row=0,column=3)
        self.btn_lp_delete.grid(row=0,column=4)

        LP_DELETE.pack()
        
        # Lets Play Create
        
        LP_CREATE = ttk.LabelFrame(W,text='Lets Play Create')
        
        self.name_var = tk.StringVar()
        self.game_name_var = tk.StringVar()
        self.episode_length_var = tk.StringVar()
        
        new_label = ttk.Label(LP_CREATE,text='Create a new Lets Play')
        name_label = ttk.Label(LP_CREATE,text='Name')
        game_name_label = ttk.Label(LP_CREATE,text='Gamename')
        name = ttk.Entry(LP_CREATE,textvariable=self.name_var)
        game_name = ttk.Entry(LP_CREATE,textvariable=self.game_name_var)
        episode_length = ttk.OptionMenu(LP_CREATE,self.episode_length_var,'None',*[f'{i} Minutes' for i in range(10,65,5)],command=self.something_changed)
        self.btn_lp_create = ttk.Button(LP_CREATE,text='create',command=self.create_lets_play)
        
        name.bind('<KeyRelease>',self.something_changed)
        game_name.bind('<KeyRelease>',self.something_changed)
        self.btn_lp_create.state(['disabled'])
        
        new_label.grid(row=0,column=1)
        name_label.grid(row = 0, column = 2)
        name.grid(row = 0, column = 3)
        game_name_label.grid(row = 0, column = 4)
        game_name.grid(row = 0, column = 5)
        episode_length.grid(row=0,column=6)
        self.btn_lp_create.grid(row=0,column=7)
    
        LP_CREATE.pack()
        
        BACKUP = ttk.LabelFrame(W,text='Lets Play Backup')
        
        self.backup_lp_label, self.backup_lp_options, self.backup_lp_option_var= get_lets_play(BACKUP, self.something_changed_backup)
        
        self.backup_btn = ttk.Button(BACKUP,text='Backup',command=self.create_video_backup)
        self.backup_btn.grid(row=0,column=3)
        self.backup_btn.state(['disabled']) 

        BACKUP.pack()
        
        W.pack()
    def load_video_backup(self,*args):
        pass
    def create_video_backup(self,*args):
        """
        Creates a ZIP archive of selected 'Let's Play' videos and TAD files.

        Disables the menu buttons during the backup process. It includes the
        TAD file and raw/final video files associated with the selected
        'Let's Play' series.
        """
        change_states([self.menu],'disabled')
        lpid = SQLAccess.read_letsplay_names().index(self.backup_lp_option_var.get())
        lpname = SQLAccess.read_letsplay_names()[lpid]
        cnef(BACKUP_FOLDER)
        ZIP = ZipFile(f'{BACKUP_FOLDER}{lpname}.7z','w',)
        tad = SQLAccess.update_tad_path(lpid)
        
        if tad is not None:
            if isfile(TAD_FOLDER+tad):
                ZIP.write(TAD_FOLDER+tad,tad)
        for ep in SQLAccess.read_episodes(lpid):#BUG
                
            for file in [
                ep.video_path,
                ep.final_video_path
                ]:
                
                if file is not None:
                    if isfile(file):
                        print(file)
                        ZIP.write(file,file.replace('\\','/').split('/')[-1])
        change_states([self.menu],'!disabled')
    
    def something_changed_backup(self, *args):
        """
        Callback for changes in the backup 'Let's Play' selection.

        Enables or disables the backup button based on whether a 'Let's Play'
        is selected.
        """
        if self.backup_lp_option_var.get() != 'None':
            self.backup_btn.state(['!disabled'])
        else:
            self.backup_btn.state(['disabled']) 
    
    def update_ui(self):
        """
        Updates UI elements related to episode range for data deletion.

        Recalculates available episode numbers based on the selected 'Let's Play'
        for the data deletion section.
        """
        lp = self.simdel_lp_option_var.get()
        if lp != 'None':
            self.epnums = [i+1 for i in range(SQLAccess.read_episode_ammount(SQLAccess.read_letsplay_names().index(self.simdel_lp_option_var.get())))]
        else:
            self.epnums = []
            
    def lp_changed(self,*args):
        """
        Callback for changes in the 'Let's Play' selection for data deletion.

        Updates the UI to reflect episode numbers for deletion, re-creates
        episode range selection widgets, and controls the state of the delete button.
        """
        self.update_ui()
        
        if not self.epnums:
            self.delete_btn.state(['disabled'])
        else:
            self.delete_btn.state(['!disabled'])
        
        self.simdel_ep_start.destroy()
        self.simdel_ep_end.destroy()
        self.simdel_label2.destroy()
        self.simdel_label3.destroy()
        self.start_btn.destroy()
        del self.epstart_option_var
        del self.epend_option_var
        
        self.simdel_label2, self.simdel_label3, self.start_btn, self.simdel_ep_start, self.simdel_ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.DATA_DELETION,lambda x: None,self.check_last_id,self.epnums)
        self.start_btn.destroy()
    
    def check_last_id(self,*args):
        """
        Validates the episode range for data deletion.

        Disables the delete button if the end episode is numerically less than
        the start episode, or if input is invalid.
        """
        if int(self.epend_option_var.get()) < int(self.epstart_option_var.get()):
            self.delete_btn.state(['disabled'])
        else:
            self.delete_btn.state(['!disabled'])
    
    def something_changed(self,*args):
        """
        Callback for changes in input fields for 'Let's Play' creation.

        Enables or disables the 'create' button based on whether all required
        fields are filled and the 'Let's Play' name is unique.
        """
        for char in self.game_name_var.get(): # See issue #236
            if char not in 'abcdefghijklmnopqrstuvwxyz_':
                self.btn_lp_create.state(['disabled'])
                return 
        
        if self.game_name_var.get() and self.name_var.get() and self.episode_length_var.get() != 'None' and self.name_var.get() not in SQLAccess.read_letsplay_names():
            self.btn_lp_create.state(['!disabled'])
            
        else:
            self.btn_lp_create.state(['disabled'])
            
    def something_changed_delete(self, *args):
        """
        Callback for changes in the 'Let's Play' selection for LP deletion.

        Enables or disables the 'delete LP' button based on whether a 'Let's Play'
        is selected.
        """
        if self.lp_option_var.get() != 'None':
            self.btn_lp_delete.state(['!disabled'])
        else:
            self.btn_lp_delete.state(['disabled']) 
            
    def create_lets_play(self,*args):
        """
        Creates a new 'Let's Play' entry in the database.

        Validates inputs, disables UI, creates the entry via SQLAccess,
        shows a success message, and then exits the application.
        """
        if self.game_name_var.get() and self.name_var.get() and self.episode_length_var.get() != 'None' and self.name_var.get() not in SQLAccess.read_letsplay_names():
            change_states([self.menu],'disabled')
            SQLAccess.create_letsplay(self.name_var.get(), self.game_name_var.get(),int(self.episode_length_var.get().split(' ')[0])*60)
            msgbox.showinfo('Success', 'Lets Play created\nYou must restart the app!')
            sys.exit()
            
    def delete_lets_play(self,*args):
        """
        Deletes a selected 'Let's Play' from the database and optionally its associated files.

        Prompts for confirmation, disables UI, deletes files if opted,
        removes the 'Let's Play' entry, shows a success message, and exits the application.
        """
        ok = msgbox.askyesno('Attention','You are trying to delete all files in the selected lets play & \nthe lets play itself!\nThis step is irreversible!\nContinue?')
        if not ok: return
        lpid = SQLAccess.read_letsplay_names.index(self.lp_option_var.get())
        if self.delete_lp_option.get():
            for ep in SQLAccess.read_episodes(lpid):#BUG
                
                for file in [
                    ep.video_path,
                    ep.thumbnail_path,
                    ep.audio_mic_edit1_path,
                    ep.audio_mic_edit2_path,
                    ep.audio_desktop_path,
                    ep.audio_mic_path,
                    ep.final_video_path
                    ]:
                    try_delete_file(file)
                    #print(ep.lpid, ep.id, )
        change_states([self.menu],'disabled')
        msgbox.showinfo('Success', 'Lets Play deleted\nYou must restart the app!')
        sys.exit()
    
    def on_detect(self,*args):
        """
        Collects and displays statistics about files and their sizes
        within various application folders.

        Calculates total files and sizes for LPRT created data, temporary files,
        raw video files, and thumbnails, then updates a label with this information.
        """
        files = 0
        files_size = 0
        temp_files = 0
        temp_files_size = 0
        for folder in (FIXED_AUDIO_FOLDER, AUDIO_FOLDER, VIDEO_FOLDER):
            for file in listdir(folder):
                files += 1
                files_size += getsize(folder+file)
        for file in listdir(TEMP_FOLDER):
            temp_files += 1
            temp_files_size += getsize(TEMP_FOLDER+file)

        video_raw_files = 0
        video_raw_files_size = 0
        thumbnail_files = 0
        thumbnail_files_size = 0
        
        for ep in SQLAccess.read_all_episodes():
            
            if isfile(ep.video_path):
                video_raw_files_size += getsize(ep.video_path)
                video_raw_files += 1
            if ep.thumbnail_path is not None:
                if isfile(ep.thumbnail_path):
                    thumbnail_files += 1
                    thumbnail_files_size += getsize(ep.thumbnail_path)
        
        TEXT = f"""
        LPRT created Data(Audio, FixedAudio, Video):  {files_size/1024/1024/1024:.2f}GB in {files} files
        Temp Files:         {temp_files_size/1024/1024/1024:.2f}GB in {temp_files} files
        Video Files(raw):   {video_raw_files_size/1024/1024/1024:.2f}GB in {video_raw_files} files
        Thumbnails:         {thumbnail_files_size/1024/1024/1024:.2f}GB in {thumbnail_files} files
        """
        
        self.label.configure(text=TEXT)
        
    def delete_files(self,*args):
        """
        Deletes episode-specific files for a selected 'Let's Play' and episode range.

        Prompts for confirmation, then iterates through the specified episode
        range and attempts to delete associated video, audio, and thumbnail files.
        """
        ok = msgbox.askyesno('Attention','You are trying to delete all files in the selected lets play\nThis step is irreversible!\nContinue?')
        if not ok: return
        lpid = SQLAccess.read_letsplay_names().index(self.simdel_lp_option_var.get())
        print(SQLAccess.read_letsplay_names().index(self.simdel_lp_option_var.get()),self.simdel_lp_option_var.get())
        episodes = SQLAccess.read_episodes(lpid)

        for i in range(*self.rng): #! Test first
            ep = episodes[i]
            for file in [
                    ep.video_path,
                    ep.thumbnail_path,
                    ep.audio_mic_edit1_path,
                    ep.audio_mic_edit2_path,
                    ep.audio_desktop_path,
                    ep.audio_mic_path,
                    ep.final_video_path
                    ]:
                print(ep.lpid)
                #try_delete_file(file)
    
    @property
    def rng(self) -> list:
        """
        Calculates the start and end indices for episode ranges.

        Returns:
            tuple: A tuple containing the start index (0-based) and end index
                   (exclusive, 0-based) for the selected episode range.
        """
        a,b = int(self.epstart_option_var.get())-1, int(self.epend_option_var.get())
        return a,b+(1 if a == b else 0)

class TBO:
    """
    A helper class for creating and managing Tkinter UI elements (Tkinter Binding Object).

    This class simplifies the creation of various Tkinter widgets (Buttons, LabeledScales,
    Entries, Checkbuttons) and binds them to Tkinter variables. It includes validation
    logic based on specified conditions (e.g., numeric ranges, non-null strings).
    """
    def __init__(self,
                 master,
                 key: str,
                 type: tk.IntVar | tk.StringVar | tk.DoubleVar, 
                 uie: ttk.Button | ttk.LabeledScale | ttk.Entry | ttk.Checkbutton, 
                 cond: str, 
                 command:bool=askopenfilename):
        self.command = command
        # cond: <62::>51 if int or double
        # cond: notnull if str
        self.master = master
        self.key: str = key
        self.type: tk.IntVar | tk.StringVar | tk.DoubleVar = type
        
        self.uie: ttk.Button | ttk.Spinbox | ttk.Entry | ttk.Checkbutton = uie

        self.var: tk.IntVar | tk.StringVar | tk.DoubleVar = self.type()
        self.cond = cond
        self.create_ui()
    
    def create_ui(self):
        """
        Creates the Tkinter UI element based on the `uie` type and packs it.

        Also binds validation checks for Entry widgets.
        """
        f = tk.Frame(self.master)
        if self.uie is ttk.Spinbox:
            ttk.Label(f,text=f'{self.name}:').grid(column=0, sticky='w')
            
            self.ui = self.uie(f,from_=self.condition[0][1:],to=self.condition[1][1:],textvariable=self.var,width=8,increment=0.1 if self.type is tk.DoubleVar else 1.0)
        elif self.uie is ttk.Entry:
            ttk.Label(f,text=f'{self.name}:').grid(column=0, sticky='w')
            self.ui = self.uie(f,textvariable=self.var)
            self.ui.bind('<KeyRelease>',self.check)
        elif self.uie is ttk.Checkbutton:
            self.ui = self.uie(f,variable=self.var,text=self.name)
        elif self.uie is ttk.Button:
            self.ui = self.uie(f,text=self.name,command=self.btn_cb)
        self.ui.grid(column=1,row=0, sticky='w')
        f.pack()
    
    @property
    def name(self) -> str:
        """ Extracts and returns the display name for the UI element from its key. """
        return self.key.split('::')[-1]
    
    @property
    def condition(self) -> tuple[str,str]:
        """
        Parses and returns the validation conditions.

        Raises:
            ValueError: If the condition string syntax is invalid for the variable type.
        """
        if self.type is tk.IntVar or self.type is tk.DoubleVar:
            cond = self.cond.split('::')
            if len(cond) != 2:
                raise ValueError(f'Length must be 2! {cond}')
            if (not cond[0].startswith('>') and not cond[0].startswith('<')) or (not cond[1].startswith('>') and not cond[1].startswith('<')):
                raise ValueError(f'Wrong Syntax! Should be < or > at the start! {cond}')
        elif self.type is tk.StringVar:
            cond = self.cond
            if cond != '' and cond != 'notnull':
                raise ValueError(f'Wrong condition should be empty or notnull. Not {cond}')
        return cond
    
    def btn_cb(self,*args):
        """
        Callback for button clicks, executing the assigned command.

        Updates the associated Tkinter variable with the command's result and
        then performs a validation check.
        """
        if self.command is askopenfilename:
            self.var.set(self.command())
        elif self.command is askcolor:
            self.var.set(self.command()[1])
        self.check()
        print(self.var.get())
        
    def _check_numeric(self,cond) -> bool:
        """
        Internal helper to check numeric values against a condition.
        """
        if cond.startswith('<'):
            return float(cond[1:]) <= self.get_value()
        elif cond.startswith('>'):
            return float(cond[1:]) >= self.get_value()
        
    def _check_text(self,cond) -> bool:
        """ Internal helper to check string values against a condition. """
        if cond == 'notnull':
            if not self.get_value():
                msgbox.showwarning('WARN','This input is flagged as notnull!')
            return not self.get_value()
        
    def get_value(self):
        """ Safely retrieves the current value from the associated Tkinter variable.

        Handles potential `ValueError` during initial retrieval for numeric types
        by setting a default. """
        try:
            return self.var.get()
        except:
            self.var.set(self.condition[0][1:])
            return self.var.get()
    
    def check(self,*args):
        """
        Performs validation checks on the UI element's value based on its type and conditions.
        Adjusts the variable's value if it falls outside the specified numeric range.
        """
        if self.type is tk.IntVar or self.type is tk.DoubleVar:
            if self._check_numeric(self.condition[0]):
                self.var.set(self.condition[0][1:])
            elif self._check_numeric(self.condition[1]):
                self.var.set(self.condition[1][1:])
        else:
            self._check_text(self.condition)
                
    def set_name(self,name: str):
        """
        Sets the display name of the UI element.

        Args:
            name (str): The new display name.
        """
        self.name = name
 
class TadEditor(tk.Frame):
    """
    Provides a graphical user interface for editing Thumbnail Automation Data (TAD) files.

    This editor allows users to configure various aspects of thumbnail generation,
    including background properties, logo placement and scaling, and text appearance.
    It integrates with 'Let's Play' selection and allows saving configurations
    and previewing generated thumbnails.
    """
    names = [
            {
                "pos": ['x','y'],
                "r_pos": [['x-from','x-to'],['y-from','y-to']],
                "r_scale": ['from','to'],
                "r_rot": ['from','to'],
                "center": None,
                "scale": None,
                "rot": None
            },
            {
                "path": None,
                "scale": None,
                "rot": None,
                "pos": ['x','y'],
                "center": None
            },
            {
                "path": None,
                "scale": None,
                "rot": None,
                "color": ['R','G','B','A'],
                "ol_color": ['R','G','B','A'],
                "size": None,
                "pos": ['x','y'],
                "center": None
            }

        ]
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        self.tg = ThumbnailGenerator()
        
        #W = ttk.Frame(self)
        W = tk.Frame(parent)
        self.menu = parent.master
        
        # Create Headers
        TAD_EDITOR = ttk.Frame(W)
        tad_editor_header = ttk.Label(W,text='TAD Editor',font=Font(W,size=16))
        
        LETSPLAY = ttk.LabelFrame(W,text='Lets Play')
        
        BACKGROUND = ttk.LabelFrame(W,text='Background')
        
        LOGO = ttk.LabelFrame(W,text='Logo')

        TEXT = ttk.LabelFrame(W,text='Text')
        
        SAVE = ttk.LabelFrame(W,text='Save')
        
        _, self.lp_options, self.lp_option_var= get_lets_play(LETSPLAY, self.lp_changed)
        
        self.tbos = []
        self.ui_elements = []
        for cheader, HEADER in zip(['bg','logo','text'],[BACKGROUND,LOGO,TEXT]):
            
            self.ui_elements.extend([TBO(HEADER,tbo,*FDS_TBO[inps]) for inps, tbo in zip(FDS_TBO,DEFAULT_TAD) if cheader == tbo.split('::')[0]])
        
        change_states([ui.ui for ui in self.ui_elements],'disabled')
        # Vartype | UIE | (from, to) or None

        # Packing
        #tad_editor_header.grid(row=0,column=1,pady=10,sticky='N')
        #TAD_EDITOR.grid(row=1,column=0,sticky='N')
        
        LETSPLAY.grid(row=0,column=0,sticky='N')
        
        BACKGROUND.grid(row=0,column=1,sticky='N')
        
        LOGO.grid(row=0,column=2,sticky='N')
        
        TEXT.grid(row=0,column=3,sticky='N')
        
        self.save_btn = ttk.Button(SAVE,text='save',command=self.save_tad)
        self.save_btn.grid(row=0,column=5)
        
        SAVE.grid(row=0,column=4,sticky='N')
        self.save_btn.state(['disabled'])
        
        W.pack()

    def set_logo_path(self,*args):
        """
        Opens a file dialog for selecting a logo image file (.png).

        Validates the selected file type and updates the corresponding
        Tkinter variable for the logo path. Shows error messages for
        invalid selections.
        """
        filepath = askopenfilename()
        if not filepath:
            msgbox.showwarning('WARN','No File selected')
            return
        if filepath.endswith('.png'):
            self.get_strings()[0].set(filepath)
        else:
            msgbox.showerror('ERROR','Wrong File Format')
        
    def set_font_path(self,*args):
        """
        Opens a file dialog for selecting a font file (.ttf or .otf).

        Validates the selected file type and updates the corresponding
        Tkinter variable for the font path. Shows error messages for
        invalid selections.
        """
        filepath = askopenfilename()
        if not filepath:
            msgbox.showwarning('WARN','No File selected')
            return
        if filepath.endswith('.ttf') or filepath.endswith('.otf'):
            self.get_strings()[1].set(filepath)
        else:
            msgbox.showerror('ERROR','Wrong File Format')
    
    def lp_changed(self,*args):
        """
        Callback for changes in the 'Let's Play' selection in the editor.

        Enables/disables UI elements, loads existing TAD data for the selected
        'Let's Play' (if available), or sets default values.
        """
        if self.lp_option_var.get() != 'None':
            self.save_btn.state(['!disabled'])
            change_states([ui.ui for ui in self.ui_elements],'!disabled')
            lpid = SQLAccess.read_letsplay_by_option_var(self)
            filepath = SQLAccess.read_tad_path(lpid)
            
            #! No JSONDecodError catch
            #! No wrong type catch[case: only if user change the data outside of lprt!]
            
            if isfile(filepath):
                DATA = json_read(filepath)
                [ui.var.set(DATA[entry]) for entry, ui in zip(DATA,self.ui_elements)]
            else:
                [ui.var.set(DEFAULT_TAD[entry]) for entry, ui in zip(DEFAULT_TAD,self.ui_elements)]
            
    def save_tad(self,*args):
        """
        Saves the current TAD settings to a JSON file and generates a preview thumbnail.

        Gathers data from UI elements, writes it to a `.json` file in the TAD_FOLDER,
        updates the database with the TAD file path, and generates a preview image
        which is then displayed in a `ThumbnailPreview` window.
        """
        #- Check final
        #- Write TAD File into TAD_FOLDER/lp_name.json
        if not hasattr(self,'tw'):
            self.tw = ThumbnailPreview()
        DATA = {key: ui.var.get() for ui, key in zip(self.ui_elements, DEFAULT_TAD)}
        lpid = SQLAccess.read_letsplay_by_option_var(self)
        lpname = SQLAccess.read_letsplay_name(lpid)
        filepath = f'{lpname}.json'
        json_write(f'{TAD_FOLDER}{filepath}',DATA)
        print(DATA)
        #- Update Database
        SQLAccess.update_tadpath(lpid, filepath)
        
        self.tg.generate(
            '123',
            None,
            SQLAccess.read_tad_path(lpid),
            f'{TEMP_FOLDER}preview.png'
        )
        
        self.tw.update_image(f'{TEMP_FOLDER}preview.png',None)



class Settings(tk.Frame):
    """
    Manages application settings, particularly for OBS (Open Broadcaster Software) integration.

    Provides UI elements for configuring OBS connection details (IP, Port, Password)
    and allows saving these settings to a JSON file.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        
        self.menu = parent.master
        
        # Create Headers
        SETTINGS = ttk.LabelFrame(W,text='OBS Settings')
        
        self.IP = tk.StringVar()
        self.PORT = tk.StringVar()
        self.PW = tk.StringVar()
        self.PW_TOGGLE = tk.IntVar()
        
        obs_ip_label = ttk.Label(SETTINGS,text='IP:')
        self.obs_ip = ttk.Entry(SETTINGS,textvariable=self.IP)
        
        obs_port_label = ttk.Label(SETTINGS,text='Port:')
        self.obs_port = ttk.Entry(SETTINGS,textvariable=self.PORT)
        
        obs_password_label = ttk.Label(SETTINGS,text='Password:')
        self.obs_password = ttk.Entry(SETTINGS,show='*',textvariable=self.PW)
        
        self.obs_ip.bind('<KeyPress>',self.obs_something_changed)
        self.obs_port.bind('<KeyPress>',self.obs_something_changed)
        self.obs_password.bind('<KeyPress>',self.obs_something_changed)
        
        self.set_settings_obs_btn = ttk.Button(SETTINGS,text='Set',command=self.set_obs_settings)
        
        self.show_pw = ttk.Checkbutton(SETTINGS,variable=self.PW_TOGGLE,text='show',command=self.toggle_pw_view)
        
        obs_ip_label.grid(row=0,column=0)
        self.obs_ip.grid(row=0,column=1)
        obs_port_label.grid(row=1,column=0)
        self.obs_port.grid(row=1,column=1)
        obs_password_label.grid(row=2,column=0)
        self.obs_password.grid(row=2,column=1)
        self.show_pw.grid(row=2,column=2)
        self.set_settings_obs_btn.grid(row=3,column=0)
        
        if isfile(ROOT+'obs_settings.json'):
            OBS_SETTINGS = json_read(ROOT+'obs_settings.json')
            self.IP.set(OBS_SETTINGS['ip'])
            self.PORT.set(OBS_SETTINGS['port'])
            self.PW.set(OBS_SETTINGS['pw'])
        self.obs_something_changed()
        
        # Packing
        SETTINGS.pack()

        W.grid(row=0,column=1)
        
    def toggle_pw_view(self,*args):
        """ Toggles the visibility of the password in the OBS password entry field. """
        if self.PW_TOGGLE.get():
            self.obs_password.configure(show="")
        else:
            self.obs_password.configure(show="*")
    
    def obs_something_changed(self,*args):
        """
        Callback for changes in OBS setting input fields.

        Enables or disables the 'Set' button based on whether all OBS
        connection details (IP, Port, Password) are filled.
        """
        if self.PW.get() and self.PORT.get() and self.IP.get():
            self.set_settings_obs_btn.state(['!disabled'])
        else:
            self.set_settings_obs_btn.state(['disabled'])
            
    def set_obs_settings(self,*args):
        """ Saves the current OBS connection settings to a JSON file. """
        
        NEW_OBS_SETTINGS = {key: DEFAULT_OBS_SETTINGS[key] for key in DEFAULT_OBS_SETTINGS}
        NEW_OBS_SETTINGS['ip'] = self.IP.get()
        NEW_OBS_SETTINGS['port'] = self.PORT.get()
        NEW_OBS_SETTINGS['pw'] = self.PW.get()
        json_write(ROOT+'obs_settings.json',NEW_OBS_SETTINGS)


class CompAndRender(tk.Frame):
    """
    Displays information about the application, including its license.

    Provides a scrollable text area to show the full license text.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = tk.Frame(parent)
        
        AUTOMATION_ROOT = ttk.Frame(W)
        
        self.normal_options = ttk.Frame(AUTOMATION_ROOT)
        
        automation_root_header = ttk.Label(W,text='Audio Compare & Render',font=Font(W,size=16))

        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(self.normal_options, self.lp_changed)
        
        self.update_ui()
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.normal_options,self.run,self.check_last_id,self.epnums)
        
        self.normal_options.pack()
        automation_root_header.pack(pady=10)
        AUTOMATION_ROOT.pack()
        self.thread = None
        self.menu = parent.master
        self.media_player = NewAudioPlayer(W,
                       [],
                       self)
        W.grid(row=0,column=1)
    
    def update_ui(self):
        """
        Updates the UI elements based on the selected 'Let's Play' series.

        This method dynamically calculates the available episode numbers
        based on the currently selected 'Let's Play' value and updates
        the internal `epnums` list.
        """
        lp = self.lp_option_var.get()
        if lp != 'None':
            self.epnums = [i+1 for i in range(SQLAccess.read_episode_ammount(SQLAccess.read_letsplay_by_option_var(self)))]
        else:
            self.epnums = []
    
    def lp_changed(self,*args):
        """
        Callback function executed when the 'Let's Play' selection changes.

        This method updates the UI based on the new 'Let's Play' selection,
        recalculates available episode numbers, and dynamically rebuilds
        the episode range selection widgets. It also adjusts the state
        of the start button.
        """
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
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.normal_options,self.run,self.check_last_id,self.epnums)
        
    def check_last_id(self,*args):
        """
        Validates the selected episode range.

        This callback is triggered when either the start or end episode
        selection changes. It disables the start button if the end episode
        is numerically less than the start episode, ensuring valid range selection.
        """
        if int(self.epend_option_var.get()) < int(self.epstart_option_var.get()):
            self.start_btn.state(['disabled'])
        else:
            self.start_btn.state(['!disabled'])
    
    def run_automation(self,*args):
        if self.thread is None and self.media_player.audio_list:
            #! Deactivate menus see issue #287
            print('Automation Start')
            change_states([self.menu],'disabled')
            change_states([self.start_btn,*self.media_player.get_ui()],'disabled')
            self.thread = Thread(target=self.__ra)
            self.thread.start()
            
        
    def __ra(self):
        render(self.media_player.audio_list,self,SQLAccess.read_letsplay_by_option_var(self))
        
        change_states([self.menu],'!disabled')
        change_states([self.start_btn,*self.media_player.get_ui()],'!disabled')
        self.thread = None
        
    def run(self,*args):
        a, b = int(self.epstart_option_var.get())-1, int(self.epend_option_var.get())
        rng = [a,b]
        
        episodes = SQLAccess.read_episodes(SQLAccess.read_letsplay_by_option_var(self)) #!<--
        from bin.data_access import Episodes
        episodes : list[Episodes]
        for i in range(*rng):
            reoc(episodes[i].audio_mic_edit2_path is None,ERROR_013)
            reoc(episodes[i].audio_desktop_path is None,ERROR_013)
            reoc(episodes[i].video_path is None,ERROR_013)
            
            reoc(not isfile(episodes[i].audio_mic_edit2_path),ERROR_007)
            reoc(not isfile(episodes[i].audio_desktop_path),ERROR_007)
            reoc(not isfile(episodes[i].video_path),ERROR_007)
        self.media_player.audio_list = [[i, episodes[i].audio_mic_edit2_path, episodes[i].audio_desktop_path, episodes[i].video_path,1.0] for i in range(*rng)]

class SetTitle(tk.Frame):
    """
    Displays information about the application, including its license.

    Provides a scrollable text area to show the full license text.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        W =tk.Frame(parent)
        
        self.menu = parent.master
        
        
        AUTOMATION_ROOT = ttk.Frame(W)
        
        self.normal_options = ttk.Frame(AUTOMATION_ROOT)
        
        automation_root_header = ttk.Label(W,text='Title Set',font=Font(W,size=16))

        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(self.normal_options, self.lp_changed)
        
        self.update_ui()
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.normal_options,self.run,self.check_last_id,self.epnums)
        
        self.normal_options.pack()
        automation_root_header.pack(pady=10)
        AUTOMATION_ROOT.pack()
        
        self.media_player = NewVideoPlayer(W, [],0,self)
        self.media_player.pack()
        
        ttk.Label(W,text='Ask Gemini for a hint',font=Font(W,size=16)).pack()
        ttk.Label(W,text='Only input keywords! e.g. Gaming, Mining...',font=Font(W,size=12)).pack()
        gemini_stuff = ttk.Frame(W)
        self.text = tk.StringVar()
        self.gemini_entry = ttk.Entry(gemini_stuff,textvariable=self.text)
        self.send_btn = ttk.Button(gemini_stuff,text='Send',command=self.send_and_receive)
        self.result_lbl = ttk.Label(gemini_stuff)
        self.gemini_entry.pack(fill=tk.X)
        self.send_btn.pack()
        self.result_lbl.pack()
        gemini_stuff.pack()
        
        W.grid(row=0,column=1)
    
    def update_ui(self):
        """
        Updates the UI elements based on the selected 'Let's Play' series.

        This method dynamically calculates the available episode numbers
        based on the currently selected 'Let's Play' value and updates
        the internal `epnums` list.
        """
        lp = self.lp_option_var.get()
        if lp != 'None':
            self.epnums = [i+1 for i in range(SQLAccess.read_episode_ammount(SQLAccess.read_letsplay_by_option_var(self)))]
        else:
            self.epnums = []
    
    def lp_changed(self,*args):
        """
        Callback function executed when the 'Let's Play' selection changes.

        This method updates the UI based on the new 'Let's Play' selection,
        recalculates available episode numbers, and dynamically rebuilds
        the episode range selection widgets. It also adjusts the state
        of the start button.
        """
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
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.normal_options,self.run,self.check_last_id,self.epnums)
        
    def check_last_id(self,*args):
        """
        Validates the selected episode range.

        This callback is triggered when either the start or end episode
        selection changes. It disables the start button if the end episode
        is numerically less than the start episode, ensuring valid range selection.
        """
        if int(self.epend_option_var.get()) < int(self.epstart_option_var.get()):
            self.start_btn.state(['disabled'])
        else:
            self.start_btn.state(['!disabled'])
            
    def run(self,*args):
        a, b = int(self.epstart_option_var.get())-1, int(self.epend_option_var.get())
        
        self.media_player.data = [i + 1 for i in range(a,b+(1 if a == b else 0))]
    
    def send_and_receive(self,*args):
        change_states([self.gemini_entry, self.send_btn],'disabled')
        Thread(target=self.__sar).start()
    def __sar(self):
        self.result_lbl.configure(text=str(send_gemini(f'Generate me a youtube title(gaming / lets play) for: {self.text.get()}')))
        change_states([self.gemini_entry, self.send_btn],'!disabled')
  
class About(tk.Frame):
    """
    Displays information about the application, including its license.

    Provides a scrollable text area to show the full license text.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        
        # Create Headers
        LICENSE = ttk.Frame(W)
        license_header = ttk.Label(W,text='License',font=Font(W,size=16))
        
        scrollbar = ttk.Scrollbar(W,orient='vertical')
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        
        text = tk.Text(LICENSE, width = 80, height = 25, wrap = tk.NONE,
                 yscrollcommand = scrollbar.set)
        
        for i in __LICENSE__.splitlines():
            text.insert(tk.END, f'{i}\n')
            
        text.pack(side=tk.TOP, fill=tk.X)
        scrollbar.config(command=text.yview)
        
        # Packing
        license_header.pack(pady=10)
        LICENSE.pack()
        
        W.pack()

if __name__ == '__main__':
    APP = TkinterApp()
    APP.mainloop()