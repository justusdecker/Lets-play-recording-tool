from bin.automations import *
from bin.constants import DISCLAIMER
from bin.data_access import on_start, LetsPlays, SQLAccess
from threading import Thread
from os.path import getsize
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from os import remove
LARGEFONT =("Verdana", 35)

on_start()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    global APP
    APP.destroy()
    APP = TkinterApp()

def try_delete_file(filepath: str | None) -> bool:
    if filepath is not None:
        if isfile(filepath):
            remove(filepath)
            return True
    return False

class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        self.geometry('800x600')
        # initializing frames to an empty array
        self.frames = {}
        for F in (Main, Recording, ThumbnailGenerate, FetchAudio, FixAudio, Send2Audacity, CompAndRender,SetTitle,Deploy, FileManager, Settings, About):
 
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
        ("FileManager", lambda : controller.show_frame(FileManager)),
        ("Settings", lambda : controller.show_frame(Settings)),
        ("About", lambda : controller.show_frame(About))
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
        
        W = ttk.Frame(self)
        
        self.menu = get_menu(self, controller)
        
        # Create Headers
        MAIN = ttk.Frame(W)
        main_header = ttk.Label(W,text='MAIN',font=Font(W,size=16))
        
        label = ttk.Label(MAIN, text =DISCLAIMER)

        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Packing
        main_header.pack(pady=10)
        MAIN.pack()

        W.grid(row=0,column=1)
        
        

class AutomationFrame(tk.Frame):
    def __init__(self, parent, controller,name: str): 
        tk.Frame.__init__(self, parent)
        self.should_not_reset = False
        self.thread = None
        self.automation_callback = None
        
        self.pb = ttk.Progressbar(self)
        self.pb.grid(sticky='SE',row = 0, column = 2)
        
        
        W = ttk.Frame(self)
        self.menu = get_menu(self, controller)
        
        # Create Headers
        THUMBNAIL_AUTOMATION = ttk.Frame(W)
        thumbnail_automation_header = ttk.Label(W,text=name,font=Font(W,size=16))

        self.THUMBNAIL_AUTOMATION = THUMBNAIL_AUTOMATION
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(THUMBNAIL_AUTOMATION, self.lp_changed)
        
        
        self.update_ui()
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(THUMBNAIL_AUTOMATION,self.run,self.check_last_id,self.epnums)
        
        
        thumbnail_automation_header.pack(pady=10)
        THUMBNAIL_AUTOMATION.pack()
        
        W.grid(row=0,column=1)
    def reset_progressbar(self):
        self.pb.destroy()
        
        self.pb = ttk.Progressbar(self)
        self.pb.grid(sticky='SE',row = 0, column = 2)
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
        
        self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self.THUMBNAIL_AUTOMATION,self.run,self.check_last_id,self.epnums)
        
    def check_last_id(self,*args):
        if int(self.epend_option_var.get()) < int(self.epstart_option_var.get()):
            self.start_btn.state(['disabled'])
        else:
            self.start_btn.state(['!disabled'])

class Recording(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.thread = None
        W = ttk.Frame(self)
        
        self.menu = get_menu(self, controller)
        
        # Create Headers
        RECORDING = ttk.Frame(W)
        recording_header = ttk.Label(W,text='Recording',font=Font(W,size=16))
        
        INFORMATION = ttk.Frame(W)
        information_header = ttk.Label(W,text='Information',font=Font(W,size=16))
        
        # Recording
        self.btn_connect = ttk.Button(RECORDING, text ="Connect to obs",command=self.get_connection)

        self.btn_connect.grid(row = 0, column=4)
        
        self.label, self.lp_options, self.lp_option_var= get_lets_play(RECORDING, self.lp_changed)
        
        # Information
        self.recording_information_label = ttk.Label(INFORMATION, text ="No Connection",font=Font(W,size=12))

        self.recording_information_label.grid(row = 0, column = 1)
        
        # Packing
        recording_header.pack(pady=10)
        RECORDING.pack()
        
        information_header.pack(pady=10)
        INFORMATION.pack()
        
        W.grid(row=0,column=1)

        # Disable connect button
        self.btn_connect.state(["disabled"])
        
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
        super().__init__(parent, controller,'Thumbnail Generator')
        self.automation_callback = GenerateThumbnailWF
        
class SetTitle(AutomationFrame):
     def __init__(self, parent, controller):
        
        super().__init__(parent, controller,'Set Title')
        self.should_not_reset = True
        self.automation_callback = TitleSetWF
    
class FetchAudio(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,'Fetch Audio')
        self.automation_callback = ExtractAudioWF
class FixAudio(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, 'Fix Audio')
        self.automation_callback = FixAudioWF
class Send2Audacity(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, 'Send2Audacity')
        self.automation_callback = SendToAudacityWF

class CompAndRender(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller,'Compare & Render')
        self.automation_callback = CompareAndRenderWF
    
class Deploy(AutomationFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, 'Deploy')
        self.automation_callback = DeployWF

class FileManager(tk.Frame):
    
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(self)
        # Menu
        self.menu = get_menu(self, controller)
        # Data Detection
        
        DATA_DETECTION = ttk.Frame(W)
        data_detection_header = ttk.Label(W,text='Data Detection',font=Font(W,size=16))
        self.detect_btn = ttk.Button(DATA_DETECTION, text='Detect',command=self.on_detect)
        self.label = ttk.Label(DATA_DETECTION,text='')
        
        
        
        self.detect_btn.grid(row=0,column=0)
        self.label.grid(row=0,column=1)
        
        data_detection_header.pack(pady=10)
        DATA_DETECTION.pack()
        

        
        
        
        # Data Deletion
        
        DATA_DELETION = ttk.Frame(W)
        self.DATA_DELETION = DATA_DELETION
        data_deletion_header = ttk.Label(W,text='Data Deletion',font=Font(W,size=16))
        # lp get
        # ep get
        
        self.simdel_lp_label, self.simdel_lp_options, self.simdel_lp_option_var= get_lets_play(DATA_DELETION, self.lp_changed)
        
        self.simdel_label2, self.simdel_label3, self.start_btn, self.simdel_ep_start, self.simdel_ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(DATA_DELETION,lambda x: None,self.check_last_id,[])
        self.start_btn.destroy()
        #self.label, self.lp_options, self.lp_option_var= get_lets_play(self, self.lp_changed)
        
        #self.label2, self.label3, self.start_btn, self.ep_start, self.ep_end, self.epstart_option_var, self.epend_option_var = get_episode_range(self,self.run,self.check_last_id,self.epnums)
        
        #! This will only delete some video_paths etc.
        
        self.delete_btn = ttk.Button(DATA_DELETION, text='Delete',command=self.delete_files)
        
        self.delete_btn.grid(row=0,column=7,pady=5)
        
        data_deletion_header.pack(pady=10)
        DATA_DELETION.pack()
        
        
        # Lets Play Delete
        LP_DELETE = ttk.Frame(W)
        data_lp_delete_header = ttk.Label(W,text='Lets Play Delete',font=Font(W,size=16))
        
        self.delete_lp_option = tk.IntVar(value=0)
        
        self.lp_label, self.lp_options, self.lp_option_var= get_lets_play(LP_DELETE, self.something_changed_delete)
        self.btn_lp_delete = ttk.Button(LP_DELETE,text='delete',command=self.delete_lets_play)
        
        self.delete_files_del_lp = ttk.Checkbutton(LP_DELETE,text='Delete Files?',variable=self.delete_lp_option, onvalue=1, offvalue=0)
        
        self.delete_files_del_lp.grid(row=0,column=3)
        self.btn_lp_delete.grid(row=0,column=4)
        
        data_lp_delete_header.pack(pady=10)
        LP_DELETE.pack()
        
        # Lets Play Create
        
        LP_CREATE = ttk.Frame(W)
        data_lp_create_header = ttk.Label(W,text='Lets Play Create',font=Font(W,size=16))
        
        self.name_var = tk.StringVar()
        self.game_name_var = tk.StringVar()
        self.episode_length_var = tk.StringVar()
        
        new_label = ttk.Label(LP_CREATE,text='Create a new Lets Play')
        
        name = ttk.Entry(LP_CREATE,textvariable=self.name_var)
        game_name = ttk.Entry(LP_CREATE,textvariable=self.game_name_var)
        episode_length = ttk.OptionMenu(LP_CREATE,self.episode_length_var,'None',*[f'{i} Minutes' for i in range(10,65,5)],command=self.something_changed)
        self.btn_lp_create = ttk.Button(LP_CREATE,text='create',command=self.create_lets_play)
        
        name.bind('<KeyPress>',self.something_changed)
        game_name.bind('<KeyPress>',self.something_changed)
        self.btn_lp_create.state(['disabled'])
        
        new_label.grid(row=0,column=1)
        name.grid(row = 0, column = 2)
        game_name.grid(row = 0, column = 3)
        episode_length.grid(row=0,column=4)
        self.btn_lp_create.grid(row=0,column=5)
        
        data_lp_create_header.pack(pady=10)
        LP_CREATE.pack()
        
        
        W.grid(row=0,column=1)
    
    def update_ui(self):
        lp = self.simdel_lp_option_var.get()
        if lp != 'None':
            
            
            self.epnums = [i+1 for i in range(SQLAccess.get_episode_ammount(SQLAccess.get_lp_names().index(self.simdel_lp_option_var.get())))]
        else:
            self.epnums = []
            
    def lp_changed(self,*args):
        
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
        if int(self.epend_option_var.get()) < int(self.epstart_option_var.get()):
            self.delete_btn.state(['disabled'])
        else:
            self.delete_btn.state(['!disabled'])
    
    def something_changed(self,*args):
        if self.game_name_var.get() and self.name_var.get() and self.episode_length_var.get() != 'None' and self.name_var.get() not in SQLAccess.get_lp_names():
            self.btn_lp_create.state(['!disabled'])
            
        else:
            self.btn_lp_create.state(['disabled'])
            
    def something_changed_delete(self, *args):
        if self.lp_option_var.get() != 'None':
            self.btn_lp_delete.state(['!disabled'])
        else:
            self.btn_lp_delete.state(['disabled']) 
            
    def create_lets_play(self,*args):
        if self.game_name_var.get() and self.name_var.get() and self.episode_length_var.get() != 'None' and self.name_var.get() not in SQLAccess.get_lp_names():
            change_states(self.menu,'disabled')
            SQLAccess.create_letsplay(self.name_var.get(), self.game_name_var.get(),int(self.episode_length_var.get().split(' ')[0])*60)
            msgbox.showinfo('Success', 'Lets Play created\nYou must restart the app!')
            exit()
            
    def delete_lets_play(self,*args):
        from bin.data_access import Episodes

        ep: Episodes
        
        ok = msgbox.askyesno('Attention','You are trying to delete all files in the selected lets play & \nthe lets play itself!\nThis step is irreversible!\nContinue?')
        if not ok: return
        if self.delete_lp_option.get():
            for ep in SQLAccess.read_all_episodes():#BUG
                
                for file in [
                    ep.video_path,
                    ep.thumbnail_path,
                    ep.audio_mic_edit1_path,
                    ep.audio_mic_edit2_path,
                    ep.audio_desktop_path,
                    ep.audio_mic_path,
                    ep.final_video_path
                    ]:
                    #try_delete_file(file)
                    print(ep.lpid, ep.id, )
        change_states(self.menu,'disabled')
        SQLAccess.delete_letsplay(SQLAccess.get_lp_names().index(self.lp_option_var.get()))
        msgbox.showinfo('Success', 'Lets Play deleted\nYou must restart the app!')
        exit()
    
    def on_detect(self,*args):
        """
        Collects file ammount & combined file size.
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
                    thumbnail_files += getsize(ep.thumbnail_path)
                    thumbnail_files_size += 1
        
        TEXT = f"""
        LPRT created Data(Audio, FixedAudio, Video):  {files_size/1024/1024/1024:.2f}GB in {files} files
        Temp Files:         {temp_files_size/1024/1024/1024:.2f}GB in {temp_files} files
        Video Files(raw):   {video_raw_files_size/1024/1024/1024:.2f}GB in {video_raw_files} files
        Thumbnails:         {thumbnail_files_size/1024/1024/1024:.2f}GB in {thumbnail_files} files
        """
        
        self.label.configure(text=TEXT)
        
    def delete_files(self,*args):
        ok = msgbox.askyesno('Attention','You are trying to delete all files in the selected lets play\nThis step is irreversible!\nContinue?')
        if not ok: return
        lpid = SQLAccess.get_lp_names().index(self.simdel_lp_option_var.get())
        print(SQLAccess.get_lp_names().index(self.simdel_lp_option_var.get()),self.simdel_lp_option_var.get())
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
        a,b = int(self.epstart_option_var.get())-1, int(self.epend_option_var.get())
        return a,b+(1 if a == b else 0)
class Settings(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(self)
        
        self.menu = get_menu(self, controller)
        
        # Create Headers
        SETTINGS = ttk.Frame(W)
        settings_header = ttk.Label(W,text='Settings',font=Font(W,size=16))
        
        # Packing
        settings_header.pack(pady=10)
        SETTINGS.pack()

        W.grid(row=0,column=1)
        
class About(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(self)
        
        self.menu = get_menu(self, controller)
        
        # Create Headers
        SETTINGS = ttk.Frame(W)
        settings_header = ttk.Label(W,text='Settings',font=Font(W,size=16))
        
        # Packing
        settings_header.pack(pady=10)
        SETTINGS.pack()
        
        from tkinterweb import HtmlFrame

        
        html_frame = HtmlFrame(SETTINGS,horizontal_scrollbar=False)
        from os import getcwd
        html_frame.load_file(f'{getcwd()}\\output.html')
        html_frame.grid(row=0)
        W.grid(row=0,column=1)

        
APP = TkinterApp()
APP.mainloop()


