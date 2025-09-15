from bin.ui.tk_frame_with_lp_ctrl import TKFrameWithLPControls
from bin.ui.ui_utils import change_states
from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
from bin.automations import GenerateThumbnailWF
from bin.data_access import SQLAccess
from bin.player_thumbnail import ThumbnailPreview
from bin.translation import gtran

class ThumbnailGenerate(TKFrameWithLPControls):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.check_for_each_option_var = tk.BooleanVar(value=False)
        
        options = ttk.LabelFrame(self.W,text=gtran("bin::ui::thumbnail_generate::options_header"))
        
        self.check_for_each_option = ttk.Checkbutton(options, text=gtran("bin::ui::thumbnail_generate::check_each"), variable=self.check_for_each_option_var)
        self.check_for_each_option.pack()
        
        preview = ttk.LabelFrame(self.W,text=gtran("bin::ui::thumbnail_generate::preview_header"))
        
        self.tp = ThumbnailPreview(preview)
        self.tp.pack()
        options.pack()
        preview.pack()
        self.thread = None
        
        #- Image Canvas to render on <- comes after refactoring player_thumbnail
        
    def run(self):
        """ opens a thread with `self.__run` """
        if self.thread is None:
            self.thread = Thread(target=self.__run)
            self.thread.start()
        
    def __run(self):
        """ Generates the Thumbnail """
        change_states([*self.lpep_picker.get_ui(),self.menu], 'disabled')
        
        a, b = int(self.lpep_picker.v_epstart.get()) , int(self.lpep_picker.v_epend.get())
        
        lp = SQLAccess.read_letsplay_by_option_var(self)
        
        GenerateThumbnailWF(lp,[a-1,b],self)
        
        change_states([*self.lpep_picker.get_ui(),self.menu], '!disabled')
        self.thread = None
    
