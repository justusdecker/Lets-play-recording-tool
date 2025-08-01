from bin.automations import *
from bin.constants import DISCLAIMER
from bin.data_access import on_start, LetsPlays, SQLAccess
from threading import Thread

import tkinter as tk
from tkinter import ttk

LARGEFONT =("Verdana", 35)

on_start()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    global APP
    APP.destroy()
    APP = TkinterApp()

class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        self.geometry('800x600')
        # initializing frames to an empty array
        self.frames = {}
        for F in (Main, Recording, ThumbnailGenerate, FetchAudio, FixAudio, Send2Audacity, CompAndRender,SetTitle,Deploy, Settings):
 
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

    
    BUILDER: list[str, function] = [
        ("Main", lambda : controller.show_frame(Main)),
        ("Recording", lambda : controller.show_frame(Recording)),
        ("ThumbnailGenerate", lambda : controller.show_frame(ThumbnailGenerate)),
        ("FetchAudio", lambda : controller.show_frame(FetchAudio)),
        ("FixAudio", lambda : controller.show_frame(FixAudio)),
        ("Send2Audacity", lambda : controller.show_frame(Send2Audacity)),
        ("CompAndRender", lambda : controller.show_frame(CompAndRender)),
        ("SetTitle", lambda : controller.show_frame(SetTitle)),
        ("Deploy", lambda : controller.show_frame(Deploy)),
        ("Settings", lambda : controller.show_frame(Settings))
    ]
    
    _ret = [ttk.Button(MENU, text =obj[0], command = obj[1]) for obj in BUILDER]# create btns based on BUILDER
    
    [obj.pack(fill="x") for i, obj in enumerate(_ret)]# Sets the position on frame for all btns
    
    MENU.grid(column=0,row=0,sticky='W')
    
    return _ret

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
    names = SQLAccess.get_lp_names()
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

    start_btn = ttk.Button(parent, text ="Run",command=run_callback)
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
        self.should_not_reset = False
        self.thread = None
        self.automation_callback = None
        
        self.pb = ttk.Progressbar(self)
        self.pb.grid(sticky='N',row = 0, column = 2)

        self.label, self.lp_options, self.lp_option_var= get_lets_play(self, self.lp_changed)
        
        
        self.update_ui()
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self,self.run,self.check_last_id,self.epnums)
        
        self.menu = get_menu(self, controller)
    def update_ui(self):
        lp = self.lp_option_var.get()
        if lp != 'None':
            
            
            self.epnums = [i+1 for i in range(SQLAccess.get_episode_ammount(SQLAccess.get_lp_opvar(self)))]
        else:
            self.epnums = []
    def run(self,*args):
        if self.thread is None:
            self.thread = Thread(target=self.__run)
            self.thread.start()
    def __run(self):
        self.start_btn.state(['disabled'])
        change_states(self.menu,'disabled')
        change_states([self.label, self.lp_options],'disabled')
        change_states([self.label2, self.label3,self.ep_end, self.ep_start],'disabled')
        a, b = int(self.epstart_option_var.get()) , int(self.epend_option_var.get())
        
        lp = SQLAccess.get_lp_opvar(self)
        self.thread = self.automation_callback(lp,[a-1,b],self)
        if not self.should_not_reset:
            
            change_states(self.menu,'!disabled')
            change_states([self.label, self.lp_options],'!disabled')
            change_states([self.label2, self.label3,self.ep_end, self.ep_start],'!disabled')

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
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(self, self.lp_changed)
        self.btn_connect.state(["disabled"])
        
        #TODO
        #! Show selected Lets Play
        #! Show current Episode
        
        self.menu = get_menu(self, controller)
    def lp_changed(self,*args):
        self.btn_connect.state(["!disabled"])
    def get_connection(self):
        self.lp_options.state(['disabled'])
        if self.thread is None:
            self.thread = Thread(target=self.__get_connection)
            self.thread.start()
    def __get_connection(self):
        
        change_states(self.menu,'disabled') # Deactivates all menu buttons for safety reasons
        
        ep = SQLAccess.read_episodes(SQLAccess.get_lp_names().index(self.lp_option_var.get()))
        self.btn_connect.state(["disabled"])
        self.btn_connect.configure(text='Try connection to OBS...')
        #! Currently Disconnecting only works by closing OBS <- mainly for safety reasons!
        obs_connect(self)

        self.btn_connect.state(["!disabled"])
        change_states(self.menu,'!disabled') # Reactivating
        self.btn_connect.configure(text='Error occured! Try again')
        self.thread = None
        self.lp_options.state(['!disabled'])
            
class ThumbnailGenerate(AutomationFrame):
     def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.automation_callback = GenerateThumbnailWF
        
class SetTitle(AutomationFrame):
     def __init__(self, parent, controller):
        
        super().__init__(parent, controller)
        self.should_not_reset = True
        self.automation_callback = TitleSetWF
    
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
    
class Deploy(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.automation_callback = DeployWF

class FileManager(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
class Settings(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        #label = ttk.Label(self, text ="Nothing here currently", font = LARGEFONT)

        #label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        self.menu = get_menu(self, controller)
        
        
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(self, self.something_changed_delete)
        self.btn_delete = ttk.Button(self,text='delete',command=self.delete_lets_play)
        self.btn_delete.grid(row=0,column=3)
        
        self.name_var = tk.StringVar()
        self.game_name_var = tk.StringVar()
        self.episode_length_var = tk.StringVar()
        new_label = ttk.Label(self,text='Create a new Lets Play')
        new_label.grid(row=2,column=1)
        name = ttk.Entry(self,textvariable=self.name_var)
        game_name = ttk.Entry(self,textvariable=self.game_name_var)
        episode_length = ttk.OptionMenu(self,self.episode_length_var,'None',*[f'{i} Minutes' for i in range(10,65,5)],command=self.something_changed)
        name.grid(row = 2, column = 2)
        name.bind('<KeyPress>',self.something_changed)
        game_name.bind('<KeyPress>',self.something_changed)
        game_name.grid(row = 2, column = 3)
        episode_length.grid(row=2,column=4)
        self.btn_create = ttk.Button(self,text='create',command=self.create_lets_play)
        self.btn_create.grid(row=2,column=5)
        self.btn_create.state(['disabled'])
    def something_changed_delete(self, *args):
        if self.lp_option_var.get() != 'None':
            self.btn_create.state(['!disabled'])
        else:
            self.btn_create.state(['disabled'])
    def something_changed(self,*args):
        if self.game_name_var.get() and self.name_var.get() and self.episode_length_var.get() != 'None' and self.name_var.get() not in SQLAccess.get_lp_names():
            self.btn_create.state(['!disabled'])
            
        else:
            self.btn_create.state(['disabled'])
    def create_lets_play(self,*args):
        if self.game_name_var.get() and self.name_var.get() and self.episode_length_var.get() != 'None' and self.name_var.get() not in SQLAccess.get_lp_names():
            change_states(self.menu,'disabled')
            SQLAccess.create_letsplay(self.name_var.get(), self.game_name_var.get(),int(self.episode_length_var.get().split(' ')[0])*60)
            msgbox.showinfo('Success', 'Lets Play created\nYou must restart the app!')
            exit()
    
    def delete_lets_play(self,*args):
        change_states(self.menu,'disabled')
        SQLAccess.delete_letsplay(SQLAccess.get_lp_names().index(self.lp_option_var.get()))
        msgbox.showinfo('Success', 'Lets Play deleted\nYou must restart the app!')
        exit()
APP = TkinterApp()
APP.mainloop()


