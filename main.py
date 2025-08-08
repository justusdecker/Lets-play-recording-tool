from bin.automations import *
from bin.constants import DISCLAIMER, __LICENSE__
from bin.data_access import on_start, LetsPlays, SQLAccess, json_write, json_read
from threading import Thread
from os.path import getsize
import tkinter as tk
import customtkinter as ctk

from tkinter import ttk
from tkinter.font import Font
from os import remove
from zipfile import ZipFile
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
LARGEFONT =("Verdana", 35)
ctk.set_appearance_mode('light')

on_start()

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
        for F in (Main, Recording, ThumbnailGenerate, FetchAudio, FixAudio, Send2Audacity, CompAndRender,SetTitle,Deploy, TadEditor,FileManager, Settings, About):
 
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
        ("TadEditor", lambda : controller.show_frame(TadEditor)),
        ("FileManager", lambda : controller.show_frame(FileManager)),
        ("Settings", lambda : controller.show_frame(Settings)),
        ("About", lambda : controller.show_frame(About))
    ]
    
    _ret = [ttk.Button(MENU, text =obj[0], command = obj[1]) for obj in BUILDER]# create btns based on BUILDER
    
    [obj.pack(fill="x") for i, obj in enumerate(_ret)]# Sets the position on frame for all btns
    
    MENU.grid(column=0,row=0,sticky='NW')
    
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
        
        self.progress_label = ttk.Label(self,)
        self.progress_label.grid(sticky='SE',row = 0, column = 2)
        
        
        
        
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
        
        BACKUP = ttk.Frame(W)
        backup_header = ttk.Label(W,text='Lets Play Backup',font=Font(W,size=16))
        
        self.backup_lp_label, self.backup_lp_options, self.backup_lp_option_var= get_lets_play(BACKUP, self.something_changed_backup)
        
        self.backup_btn = ttk.Button(BACKUP,text='Backup',command=self.create_video_backup)
        self.backup_btn.grid(row=0,column=3)
        self.backup_btn.state(['disabled']) 
        
        backup_header.pack(pady=10)
        BACKUP.pack()
        
        W.grid(row=0,column=1)
    
    def create_video_backup(self,*args):
        change_states(self.menu,'disabled')
        lpid = SQLAccess.get_lp_names().index(self.backup_lp_option_var.get())
        lpname = SQLAccess.get_lp_names()[lpid]
        cnef(BACKUP_FOLDER)
        ZIP = ZipFile(f'{BACKUP_FOLDER}{lpname}.7z','w',)
        tad = SQLAccess.get_tad_path(lpid)
        
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
        change_states(self.menu,'!disabled')

                
        
        
        
    
    def something_changed_backup(self, *args):
        if self.backup_lp_option_var.get() != 'None':
            self.backup_btn.state(['!disabled'])
        else:
            self.backup_btn.state(['disabled']) 
    
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
        lpid = SQLAccess.get_lp_names().index(self.lp_option_var.get())
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
        change_states(self.menu,'disabled')
        #! Deleting Lets Play 
        #! SQLAccess.delete_letsplay(SQLAccess.get_lp_names().index(self.lp_option_var.get()))
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
        settings_header = ttk.Label(W,text='OBS Settings',font=Font(W,size=16))
        
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
        
        self.show_pw = ttk.Checkbutton(SETTINGS,variable=self.PW_TOGGLE,command=self.toggle_pw_view)
        
        obs_ip_label.grid(row=0,column=0)
        self.obs_ip.grid(row=0,column=1)
        obs_port_label.grid(row=0,column=2)
        self.obs_port.grid(row=0,column=3)
        obs_password_label.grid(row=0,column=4)
        self.obs_password.grid(row=0,column=5)
        self.show_pw.grid(row=0,column=6)
        self.set_settings_obs_btn.grid(row=0,column=7)
        
        if isfile(ROOT+'obs_settings.json'):
            OBS_SETTINGS = json_read(ROOT+'obs_settings.json')
            self.IP.set(OBS_SETTINGS['ip'])
            self.PORT.set(OBS_SETTINGS['port'])
            self.PW.set(OBS_SETTINGS['pw'])
        self.obs_something_changed()
        
        # Packing
        settings_header.pack(pady=10)
        SETTINGS.pack()

        W.grid(row=0,column=1)
        
    def toggle_pw_view(self,*args):
        if self.PW_TOGGLE.get():
            self.obs_password.configure(show="")
        else:
            self.obs_password.configure(show="*")
    def obs_something_changed(self,*args):
        if self.PW.get() and self.PORT.get() and self.IP.get():
            self.set_settings_obs_btn.state(['!disabled'])
        else:
            self.set_settings_obs_btn.state(['disabled'])
    def set_obs_settings(self,*args):
        print('Updated OBS Settings')
        
        NEW_OBS_SETTINGS = {key: DEFAULT_OBS_SETTINGS[key] for key in DEFAULT_OBS_SETTINGS}
        NEW_OBS_SETTINGS['ip'] = self.IP.get()
        NEW_OBS_SETTINGS['port'] = self.PORT.get()
        NEW_OBS_SETTINGS['pw'] = self.PW.get()
        json_write(ROOT+'obs_settings.json',NEW_OBS_SETTINGS)


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




INPUT_INT_NV = (tk.IntVar,ttk.Entry, '>-2048::<2048')
INPUT_SCALE = (tk.DoubleVar,ttk.LabeledScale, '>-0.5::<3.5')
INPUT_ROT = (tk.DoubleVar,ttk.LabeledScale, '>-359::<359')
INPUT_CB = (tk.IntVar,ttk.Checkbutton, '')
INPUT_COLOR = (tk.IntVar,ttk.Entry, '>-1::<256') #! Will be changed later
FDS_TBO = {
    "bg::pos::x": INPUT_INT_NV,
    "bg::pos::y": INPUT_INT_NV,
    "bg::r_pos::x-from": INPUT_INT_NV,
    "bg::r_pos::x-to": INPUT_INT_NV,
    "bg::r_pos::y-from": INPUT_INT_NV,
    "bg::r_pos::y-to": INPUT_INT_NV,
    "bg::r_scale::from": INPUT_SCALE,
    "bg::r_scale::to": INPUT_SCALE,
    "bg::r_rot::from": INPUT_ROT,
    "bg::r_rot::to": INPUT_ROT,
    "bg::center": INPUT_CB,
    "bg::scale": INPUT_SCALE,
    "bg::rot": INPUT_ROT,

    "logo::path": (tk.StringVar,ttk.Button, 'notnull'),
    "logo::scale": INPUT_SCALE,
    "logo::rot": INPUT_ROT,
    "logo::pos::x": INPUT_INT_NV,
    "logo::pos::y": INPUT_INT_NV,
    "logo::center": INPUT_CB,

    "text::path": (tk.StringVar,ttk.Button, ''),
    "text::scale": INPUT_SCALE,
    "text::rot": INPUT_ROT,
    "text::color": (tk.StringVar,ttk.Button, 'notnull',askcolor),
    "text::ol_color": (tk.StringVar,ttk.Button, 'notnull',askcolor),
    "text::size": INPUT_INT_NV,
    "text::pos::x": INPUT_INT_NV,
    "text::pos::y": INPUT_INT_NV,
    "text::center": INPUT_CB
}

class TBO:
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
        
        self.uie: ttk.Button | ttk.LabeledScale | ttk.Entry | ttk.Checkbutton = uie

        self.var: tk.IntVar | tk.StringVar | tk.DoubleVar = self.type()
        self.cond = cond
        self.create_ui()
    def create_ui(self):

        if self.uie is ttk.LabeledScale:
            ttk.Label(self.master,text=f'{self.name}:').pack()
            self.ui = self.uie(self.master,from_=self.condition[0][1:],to=self.condition[1][1:],variable=self.var)
        elif self.uie is ttk.Entry:
            ttk.Label(self.master,text=f'{self.name}:').pack()
            self.ui = self.uie(self.master,textvariable=self.var)
            self.ui.bind('<KeyRelease>',self.check)
        elif self.uie is ttk.Checkbutton:
            self.ui = self.uie(self.master,variable=self.var,text=self.name)
        elif self.uie is ttk.Button:
            self.ui = self.uie(self.master,text=self.name,command=self.btn_cb)
        self.ui.pack()
    @property
    def name(self) -> str:
        return self.key.split('::')[-1]
    @property
    def condition(self) -> tuple[str,str]:
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
        if self.command is askopenfilename:
            self.var.set(self.command())
        elif self.command is askcolor:
            self.var.set(self.command()[1])
        self.check()
        print(self.var.get())
    def _check_numeric(self,cond) -> bool:
        if cond.startswith('<'):
            return float(cond[1:]) >= self.get_value()
        elif cond.startswith('>'):
            return float(cond[1:]) <= self.get_value()
    def _check_text(self,cond) -> bool:
        if cond == 'notnull':
            if not self.get_value():
                msgbox.showwarning('WARN','This input is flagged as notnull!')
            return not self.get_value()
    def get_value(self):
        try:
            return self.var.get()
        except:
            self.var.set(self.condition[0][1:])
            return self.var.get()
    def check(self,*args):
        if self.type is tk.IntVar or self.type is tk.DoubleVar:
            if self._check_numeric(self.condition[0]):
                self.var.set(self.condition[0][1:])
            elif self._check_numeric(self.condition[1]):
                self.var.set(self.condition[1][1:])
        else:
            self._check_text(self.condition)
                
        
    def set_name(self,name: str):
        self.name = name
 
class TadEditor(tk.Frame):#! REWORK HERE
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
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.tg = ThumbnailGenerator()
        #W = ttk.Frame(self)
        W = ctk.CTkScrollableFrame(self,width=600,height=400)
        self.menu = get_menu(self, controller)
        
        # Create Headers
        TAD_EDITOR = ttk.Frame(W)
        tad_editor_header = ttk.Label(W,text='TAD Editor',font=Font(W,size=16))
        
        LETSPLAY = ttk.Frame(W)
        letsplay_header = ttk.Label(W,text='Lets Play',font=Font(W,size=14))
        
        BACKGROUND = ttk.Frame(W)
        background_header = ttk.Label(W,text='Background',font=Font(W,size=14))
        
        LOGO = ttk.Frame(W)
        logo_header = ttk.Label(W,text='Logo',font=Font(W,size=14))

        TEXT = ttk.Frame(W)
        text_header = ttk.Label(W,text='Text',font=Font(W,size=14))
        
        SAVE = ttk.Frame(W)
        save_header = ttk.Label(W,text='Save',font=Font(W,size=14))
        
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
        
        letsplay_header.grid(row=0,column=0,pady=10,sticky='N')
        LETSPLAY.grid(row=1,column=0,sticky='N')
        
        background_header.grid(row=0,column=1,pady=10,sticky='N')
        BACKGROUND.grid(row=1,column=1,sticky='N')
        
        logo_header.grid(row=0,column=2,pady=10,sticky='N')
        LOGO.grid(row=1,column=2,sticky='N')
        
        text_header.grid(row=0,column=3,pady=10,sticky='N')
        TEXT.grid(row=1,column=3,sticky='N')
        
        self.save_btn = ttk.Button(SAVE,text='save',command=self.save_tad)
        self.save_btn.grid(row=0,column=5)
        
        save_header.grid(row=0,column=4,pady=10,sticky='N')
        SAVE.grid(row=1,column=4,sticky='N')
        self.save_btn.state(['disabled'])
        
        W.grid(row=0,column=1)

    def set_logo_path(self,*args):
        filepath = askopenfilename()
        if not filepath:
            msgbox.showwarning('WARN','No File selected')
            return
        if filepath.endswith('.png'):
            self.get_strings()[0].set(filepath)
        else:
            msgbox.showerror('ERROR','Wrong File Format')
        
       
    def set_font_path(self,*args):
        filepath = askopenfilename()
        if not filepath:
            msgbox.showwarning('WARN','No File selected')
            return
        if filepath.endswith('.ttf') or filepath.endswith('.otf'):
            self.get_strings()[1].set(filepath)
        else:
            msgbox.showerror('ERROR','Wrong File Format')
    def lp_changed(self,*args):
        if self.lp_option_var.get() != 'None':
            self.save_btn.state(['!disabled'])
            change_states([ui.ui for ui in self.ui_elements],'!disabled')
            lpid = SQLAccess.get_lp_opvar(self)
            filepath = SQLAccess.get_tad_path(lpid)
            
            #! No JSONDecodError catch
            #! No wrong type catch[case: only if user change the data outside of lprt!]
            
            if isfile(filepath):
                DATA = json_read(filepath)
                [ui.var.set(DATA[entry]) for entry, ui in zip(DATA,self.ui_elements)]
            else:
                [ui.var.set(DEFAULT_TAD[entry]) for entry, ui in zip(DEFAULT_TAD,self.ui_elements)]
            
    def save_tad(self,*args):
        #- Check final
        #- Write TAD File into TAD_FOLDER/lp_name.json
        DATA = {key: ui.var.get() for ui, key in zip(self.ui_elements, DEFAULT_TAD)}
        lpid = SQLAccess.get_lp_opvar(self)
        lpname = SQLAccess.get_lp_name(lpid)
        filepath = f'{lpname}.json'
        json_write(filepath,DATA)
        print(DATA)
        #- Update Database
        SQLAccess.set_tadpath(lpid, filepath)
        self.tg.generate(
            '123',
            None,
            SQLAccess.get_tad_path(lpid),
            f'{TEMP_FOLDER}preview.png'
        )

class About(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(self)
        
        self.menu = get_menu(self, controller)
        
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
        
        W.grid(row=0,column=1)
    
APP = TkinterApp()
APP.mainloop()


