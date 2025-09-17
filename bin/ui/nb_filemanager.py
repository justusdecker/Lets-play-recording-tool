from bin.xmsgbox import xinf, xerr, xqu
import tkinter as tk
import tkinter.ttk as ttk
from tools.log import LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
from bin.data_access import SQLAccess, AsciiImage,cnef, try_delete_file, csv_read, csv_write
from os.path import getsize, isdir,isfile
from os import listdir
import sys
from zipfile import ZipFile
from bin.constants import (
    ICO_TRASH,
    ICO_NEW,
    ICO_REFRESH,
    ICO_BACKUP,
    ICO_SEARCH,
    BACKUP_FOLDER,
    TAD_FOLDER,
    ROOT,
    TEMP_FOLDER,
    THUMBNAIL_FOLDER,
    DEPLOY_FOLDER,
    AUDIO_FOLDER,
    FIXED_AUDIO_FOLDER,
    AC_RESULT_FOLDER)
from subprocess import Popen
from bin.ui.lpep_picker import LPEPPicker
from bin.ui.ui_utils import change_states
from bin.translation import gtran
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
        open_folder_btn = ttk.Button(W,text=gtran("bin::ui::filemanager::open_lprt_folder"),command=lambda *x: Popen(f'explorer {ROOT}'))
        open_folder_btn.pack()
        DATA_DETECTION = ttk.LabelFrame(W,text=gtran("bin::ui::filemanager::data_detection_header"))
        img = AsciiImage(ICO_SEARCH)
        self.detect_btn = ttk.Button(DATA_DETECTION, image=img.image,command=self.on_detect)
        self.label = ttk.Label(DATA_DETECTION,text='')
        self.label.image = img.image
        self.detect_btn.grid(row=0,column=0)
        self.label.grid(row=0,column=1)
        DATA_DETECTION.pack()
        
        # Data Deletion
        
        DATA_DELETION = ttk.LabelFrame(W,text=gtran("bin::ui::filemanager::data_deletion_header"))
        self.DATA_DELETION = DATA_DELETION
        
        self.simple_delete_lpep = LPEPPicker(DATA_DELETION,self.delete_files,'lp-ep',ICO_TRASH)
        
        DATA_DELETION.pack()
        
        # Lets Play Create
        
        LP_CREATE = ttk.LabelFrame(W,text=gtran("bin::ui::filemanager::lp_create_header"))
        
        self.name_var = tk.StringVar()
        self.game_name_var = tk.StringVar()
        self.episode_length_var = tk.StringVar()
        
        new_label = ttk.Label(LP_CREATE,text=gtran("bin::ui::filemanager::lp_create_label_0"))
        name_label = ttk.Label(LP_CREATE,text=gtran("bin::ui::filemanager::lp_create_label_1"))
        game_name_label = ttk.Label(LP_CREATE,text=gtran("bin::ui::filemanager::lp_create_label_2"))
        name = ttk.Entry(LP_CREATE,textvariable=self.name_var)
        game_name = ttk.Entry(LP_CREATE,textvariable=self.game_name_var)
        episode_length = ttk.OptionMenu(LP_CREATE,self.episode_length_var,'None',*[f'{i} {gtran("bin::ui::filemanager::lp_minutes")}' for i in range(10,65,5)],command=self.something_changed)
        img = AsciiImage(ICO_NEW)
        self.btn_lp_create = ttk.Button(LP_CREATE,image=img.image,command=self.create_lets_play)
        self.btn_lp_create.image = img.image
        self.btn_lp_create.state(['disabled'])
        
        new_label.grid(row=0,column=1)
        name_label.grid(row = 0, column = 2)
        name.grid(row = 0, column = 3)
        game_name_label.grid(row = 0, column = 4)
        game_name.grid(row = 0, column = 5)
        episode_length.grid(row=0,column=6)
        self.btn_lp_create.grid(row=0,column=7)
    
        LP_CREATE.pack()
        
        LP_EDIT = ttk.LabelFrame(W,text=gtran("bin::ui::filemanager::lp_edit_header"))
        
        self.lp_edit_lpep = LPEPPicker(LP_EDIT,self.update_lets_play,'lp',ICO_REFRESH)

        self.lp_edit_episode_length_var = tk.StringVar()

        lp_edit_episode_length = ttk.OptionMenu(LP_EDIT,self.lp_edit_episode_length_var,'None',*[f'{i} {gtran("bin::ui::filemanager::lp_minutes")}' for i in range(10,65,5)])
        img = AsciiImage(ICO_REFRESH)

        lp_edit_episode_length.pack()

        LP_EDIT.pack()
        
        BACKUP = ttk.LabelFrame(W,text=gtran("bin::ui::filemanager::lp_backup_header"))
        
        self.backup_lpep = LPEPPicker(BACKUP,self.create_video_backup,'lp', ICO_BACKUP)

        BACKUP.pack()
        
        
        # Export
        
        EXPORT = ttk.LabelFrame(W,text=gtran("bin::ui::filemanager::export_header"))
        ttk.Button(EXPORT,text=gtran("bin::ui::filemanager::export_header"),command=self.export).pack()
        EXPORT.pack()
        
        IMPORT = ttk.LabelFrame(W,text=gtran("bin::ui::filemanager::import_header"))
        ttk.Button(IMPORT,text=gtran("bin::ui::filemanager::import_header"),command=self.import_).pack()
        IMPORT.pack()
        W.pack()
    def export(self, *_):
        SQLAccess.export_lpep()

    def import_(self, *_):
        SQLAccess.create_from_csv()
        xinf('Successfully imported files. Closing App.') # TODO - Translation
        sys.exit()
        
        
    def update_lets_play(self,*_):
        """ Updates the episode_length for the selected lets-play only if value is not None """
        if self.lp_edit_lpep.v_lp.get() == 'None': return
        SQLAccess.update_letsplay(SQLAccess.read_letsplay_names().index(self.lp_edit_lpep.v_lp.get()),int(self.lp_edit_episode_length_var.get().split(' ')[0])*60)
    
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
             
    def load_video_backup(self,*args):
        """
        See issue #212
        """
        
    def create_video_backup(self,*args):
        """
        Creates a ZIP archive of selected 'Let's Play' videos and TAD files.

        Disables the menu buttons during the backup process. It includes the
        TAD file and raw/final video files associated with the selected
        'Let's Play' series.
        """
        change_states([self.menu],'disabled')
        lpid = SQLAccess.read_letsplay_names().index(self.backup_lpep.v_lp.get())
        lpname = SQLAccess.read_letsplay_names()[lpid]
        cnef(BACKUP_FOLDER)
        ZIP = ZipFile(f'{BACKUP_FOLDER}{lpname}.7z','w',)
        tad = SQLAccess.read_tad_path(lpid)
        try:
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
        except Exception as E:
            xerr( str(E))
        change_states([self.menu],'!disabled')

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

    def create_lets_play(self,*args):
        """
        Creates a new 'Let's Play' entry in the database.

        Validates inputs, disables UI, creates the entry via SQLAccess,
        shows a success message, and then exits the application.
        """
        if self.game_name_var.get() and self.name_var.get() and self.episode_length_var.get() != 'None' and self.name_var.get() not in SQLAccess.read_letsplay_names():
            change_states([self.menu],'disabled')
            SQLAccess.create_letsplay(self.name_var.get(), self.game_name_var.get(),int(self.episode_length_var.get().split(' ')[0])*60)
            xinf(gtran("bin::ui::filemanager::something_changed"))
            sys.exit()
    
    def det(self,path: str) -> list[str,int,int]:
        """ 
        Goes trough folder/sub_folder(<- if exist) & adding up the size & ammount of files.
        
        Returns:
            str: formatted {SIZE} in {AMMOUNT} files
            
            int: SIZE
            
            int: AMMOUNT
        """
        SIZE = 0
        AMMOUNT = 0
        for file in listdir(path):
            try:
                if isfile(f'{path}{file}'):
                    SIZE += getsize(f'{path}{file}')
                    AMMOUNT += 1
                if isdir(f'{path}{file}'):
                    for subfile in listdir(f'{path}{file}\\'):
                        SIZE += getsize(f'{path}{file}\\{subfile}')
                        AMMOUNT += 1
            except Exception as E:
                print(E)
            
        return f'{self.gsn(SIZE)} in {AMMOUNT} files',SIZE, AMMOUNT
    
    def gsn(self,num: int) -> str:
        """
        Converts a number of bytes into a human-readable size string.

        This method takes a numerical value representing bytes and converts it
        into a more readable format (e.g., KB, MB, GB, TB) by dividing by 1024
        until the number is less than 1024. The result is formatted to two
        decimal places and appended with the appropriate unit.
        """
        typ = ['B','KB','MB','GB','TB']
        if num:
            while 1:
                if int(num/1024):
                    num /= 1024
                    typ.pop(0)
                else:
                    break
        return f'{num:.2f}{typ[0]}'
    
    def on_detect(self,*args):
        """
        Collects and displays statistics about files and their sizes
        within various application folders.

        Calculates total files and sizes for all LPRT related data, then updates a label with this information.
        """

        results = {
            'temp': self.det(TEMP_FOLDER),
            'thumbnails': self.det(THUMBNAIL_FOLDER),
            'audio': self.det(AUDIO_FOLDER),
            'audio_fixed': self.det(FIXED_AUDIO_FOLDER),
            'ac_results': self.det(AC_RESULT_FOLDER),
            'deploy': self.det(DEPLOY_FOLDER)
        }
        video_files = 0
        video_size = 0
        for ep in SQLAccess.read_all_episodes():
            if isfile(ep.video_path):
                video_size += getsize(ep.video_path)
                video_files += 1
        results['video_raw'] = (f'{self.gsn(video_size)} -> {video_files} {gtran("bin::ui::filemanager::files")}', video_size,video_files)
        ALL = f""        
        tot_f, tot_s = 0, 0
        for key in results:
            ALL += f'{key:<10} {results[key][0]}\n'
            tot_f += results[key][2]
            tot_s += results[key][1]
        ALL += f'{gtran("bin::ui::filemanager::total")} {self.gsn(tot_s)} in {tot_f} {gtran("bin::ui::filemanager::files")}'
        
        self.label.configure(text=ALL)
        
    def delete_files(self,*args):
        """
        Deletes episode-specific files for a selected 'Let's Play' and episode range.

        Prompts for confirmation, then iterates through the specified episode
        range and attempts to delete associated video, audio, and thumbnail files.
        """
        
        
        lpid = SQLAccess.read_letsplay_names().index(self.simple_delete_lpep.v_lp.get())
        LOG(f"Delete: [$][$ - $]",[SQLAccess.read_letsplay_name(lpid),*self.rng])
        ok = xqu(gtran("bin::ui::filemanager::warning"))
        if not ok: return
        #print(SQLAccess.read_letsplay_names().index(self.simple_delete_lpep.v_lp.get()),self.simple_delete_lpep.v_lp.get())
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
                try:
                    if try_delete_file(file):
                        LOG(f'($)Removed: $ - of $ | $',[i+1, file, lpid, SQLAccess.read_letsplay_game_name(lpid)],LOG_INFO)
                    else:
                        LOG(f'($)Does not exist(skip): $ - of $ | $',[i+1, file, lpid, SQLAccess.read_letsplay_game_name(lpid)],LOG_WARNING)
                except Exception as E:
                    LOG(f'($)Failed: $ - of $ | $ - $',[i+1, file, lpid, SQLAccess.read_letsplay_game_name(lpid), E],LOG_ERROR)
    
    @property
    def rng(self) -> list:
        """
        Calculates the start and end indices for episode ranges.

        Returns:
            tuple: A tuple containing the start index (0-based) and end index
                   (exclusive, 0-based) for the selected episode range.
        """
        a,b = int(self.simple_delete_lpep.v_epstart.get())-1, int(self.simple_delete_lpep.v_epend.get())
        return a,b+(1 if a == b else 0)
