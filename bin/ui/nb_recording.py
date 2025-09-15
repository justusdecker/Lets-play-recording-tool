import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
from bin.translation import gtran
from bin.ui.lpep_picker import LPEPPicker
from bin.ui.ui_utils import change_states
from bin.automations import obs_connect
from threading import Thread
class Recording(tk.Frame):
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        self.thread = None
        W = ttk.Frame(parent)
        
        self.menu = parent.master
        
        # Create Headers
        RECORDING = ttk.LabelFrame(W,text=gtran("bin::ui::recording_header"))
        
        INFORMATION = ttk.LabelFrame(W,text=gtran("bin::ui::recording_information_header"))

        
        # Recording
        self.btn_connect = ttk.Button(RECORDING, text =gtran("bin::ui::connect_btn_text_default"),command=self.get_connection)

        self.btn_connect.pack(side='bottom')
        
        self.lpep_picker = LPEPPicker(RECORDING,False,'lp-nb',ch_callback=self.lp_changed)
        
        # Information
        self.recording_information_label = ttk.Label(INFORMATION, text ="No Connection",font=tk.font.Font(W,size=12))

        self.recording_information_label.grid(row = 0, column = 1)
        
        # Packing
        RECORDING.pack()
        INFORMATION.pack()
        
        W.pack()

        # Disable connect button
        self.btn_connect.state(["disabled"])
        
    def lp_changed(self,*args):
        self.btn_connect.state(["!disabled"])
    def get_connection(self):
        """ This launched the thread, to get OBS connection """
        if self.thread:
            self.close_connection = True
        change_states(self.lpep_picker.get_ui(),'disabled')
        if self.thread is None:
            self.close_connection = False
            self.thread = Thread(target=self.__get_connection)
            self.thread.start()
    def __get_connection(self):
        """ Establish the connection & terminates it - with obs """
        change_states([self.menu],'disabled') # Deactivates all menu buttons for safety reasons
        self.btn_connect.state(["disabled"])
        self.btn_connect.configure(text='Try connection to OBS...')
        obs_connect(self)

        self.btn_connect.state(["!disabled"])
        change_states([self.menu],'!disabled') # Reactivating
        if not self.close_connection:
            self.btn_connect.configure(text='Error occured! Try again')
        self.thread = None
        change_states(self.lpep_picker.get_ui(),'!disabled')
 