from tkinter import ttk
import tkinter as tk
from tkinter.font import Font
from bin.constants import *
from bin.constants import __LICENSE__
from bin.data_access import SQLAccess, AsciiImage
from threading import Thread
from bin.welcome_popup import WELCOME
from bin.automations import *

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
        self.geometry('800x600')
        self.build_ui()
        WELCOME.destroy()
    def get_ui_names(self) -> list[str]:
        return [
            'Main',
            'Recording',
            'ThumbnailGenerate',
            'FetchAudio',
            'About',
            'Recording'
        ]
    def build_ui(self):
        ELEMENTS = [
            (Main, 'Main'),
            (Recording, 'Recording'),
            (ThumbnailGenerate,'ThumbnailGenerate'),
            (FetchAudio,'FetchAudio'),
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
        
        W = tk.Frame(self)
        
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