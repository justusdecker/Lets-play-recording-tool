import tkinter as tk
import tkinter.ttk as ttk
from bin.data_access import SQLAccess, reoc, isfile
from bin.constants import ERROR_007, ERROR_013
from threading import Thread
from bin.ui.lpep_picker import LPEPPicker
from bin.player_audio import NewAudioPlayer
from bin.ui.ui_utils import change_states
from bin.automations import render
class CompAndRender(tk.Frame):
    """
    Displays information about the application, including its license.

    Provides a scrollable text area to show the full license text.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = tk.Frame(parent)
        
        AUTOMATION_ROOT = ttk.Frame(W)
        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        self.lpep_picker = LPEPPicker(AUTOMATION_ROOT,self.run,'lp-ep')
        AUTOMATION_ROOT.pack()
        self.thread = None
        self.menu = parent.master
        self.media_player = NewAudioPlayer(W,
                       [],
                       self)
        W.grid(row=0,column=1)
    
    def run_automation(self,*args):
        """ Run a thread with `self.__ra` """
        if self.thread is None and self.media_player.audio_list:
            #! Deactivate menus see issue #287
            print('Automation Start')
            change_states([*self.media_player.get_ui(),*self.lpep_picker.get_ui(),self.menu],'disabled')
            self.thread = Thread(target=self.__ra)
            self.thread.start()
            
    def __ra(self):
        """ This will render your video """
        render(self.media_player.audio_list,self,SQLAccess.read_letsplay_by_option_var(self))
        
        change_states([*self.media_player.get_ui(),*self.lpep_picker.get_ui(),self.menu],'!disabled')
        self.thread = None
        
    def run(self,*args):
        """ This updates the `audio_list` in the AudioPlayer """
        a, b = int(self.lpep_picker.v_epstart.get())-1, int(self.lpep_picker.v_epend.get())
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
        audio_list = [[i, episodes[i].audio_mic_edit2_path, episodes[i].audio_desktop_path, episodes[i].video_path,1.0] for i in range(*rng)]
        self.media_player.reset(audio_list)
