from bin.automations_new import *
from bin.data_access import LetsPlay, Episode
from threading import Thread
LP_PATH = 'lets_plays.csv'

import tkinter as tk
from tkinter import ttk

LARGEFONT =("Verdana", 35)

class Locks:
    MENU_FORBIDDEN = False
    OBS_RECORD = False
    OBS_CONNECTED = False
LOCKS = Locks()

DISCLAIMER = """
Welcome to LPRT

This Tool is currently Work in Progress!
Some features might not work as expected & can cause data loss! Be careful!
"""




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
    from a `LetsPlay` object which conceptually reads from 'lets_plays.csv'.
    When a selection is made, the provided `callback` function is executed.
    """
    label = ttk.Label(parent, text ="Lets Play")

    label.grid(row = 0, column = 1) 
    
    lp_option_var = tk.StringVar(parent)
        
    lps = LetsPlay('lets_plays.csv')
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

        get_menu(self, controller)

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
            self.epnums = [i+1 for i in range(Episode(ep_path).row)]
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
        self.label = ttk.Label(self, text ="No Connection", font = LARGEFONT)

        self.label.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        self.btn_connect = ttk.Button(self, text ="Connect to obs",command=self.get_connection)

        self.btn_connect.grid(row = 0, column=2)
        
        #TODO
        #! Show selected Lets Play
        #! Show current Episode
        
        self.menu = get_menu(self, controller)
    def get_connection(self):
        if self.thread is None:
            self.thread = Thread(target=self.__get_connection)
            self.thread.start()
    def __get_connection(self):
        
        change_states(self.menu,'disabled') # Deactivates all menu buttons for safety reasons
        ep = LetsPlay(LP_PATH).get_episodes(0)
        self.btn_connect.state(["disabled"])
        self.btn_connect.configure(text='Try connection to OBS...')
        #! Currently Disconnecting only works by closing OBS <- mainly for safety reasons!
        obs_connect(ep,self)

        self.btn_connect.state(["!disabled"])
        change_states(self.menu,'!disabled') # Reactivating
        self.btn_connect.configure(text='Error occured! Try again')
        self.thread = None
            
class ThumbnailGenerate(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="ThumbnailGenerate", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        get_menu(self, controller)
    
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
        
        
        label = ttk.Label(self, text ="Settings", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        self.menu = get_menu(self, controller)
        

app = TkinterApp()
app.mainloop()


