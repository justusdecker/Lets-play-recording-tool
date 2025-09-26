import tkinter as tk
import tkinter.ttk as ttk
from bin.ui.lpep_picker import LPEPPicker
from threading import Thread
from bin.data_access import SQLAccess
from bin.ui.ui_utils import change_states
from bin.ui.progress_bar_manager import ProgressBarManager

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

        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        
        self.lpep_picker = LPEPPicker(AUTOMATION_ROOT,self.run,'lp-ep')
        
        self.pbm = ProgressBarManager(AUTOMATION_ROOT)

        AUTOMATION_ROOT.pack()
        
        W.pack()
               
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
        change_states([*self.lpep_picker.get_ui(), self.menu],'disabled')
        a, b = int(self.lpep_picker.v_epstart.get()) , int(self.lpep_picker.v_epend.get())
        
        lp = SQLAccess.read_letsplay_by_option_var(self)
        self.automation_callback(lp,[a-1,b],self)
        
        if not self.should_not_reset:
            
            change_states([*self.lpep_picker.get_ui(), self.menu],'!disabled')

        self.thread = None
        