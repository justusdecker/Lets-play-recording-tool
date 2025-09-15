from bin.constants import VERSION, HASH
import tkinter as tk
from bin.ui.notebook import Notebook
from bin.welcome_popup import WELCOME
from bin.data_access import AsciiImage
from bin.constants import IMG_LOGO
from bin.translation import gtran
from tools.log import LOG

from bin.ui.nb_main import Main
from bin.ui.nb_fix_audio import FixAudio
from bin.ui.nb_fetch_audio import FetchAudio
from bin.ui.nb_deploy import Deploy
from bin.ui.nb_recording import Recording
from bin.ui.nb_thumbnail_generate import ThumbnailGenerate
from bin.ui.nb_send_to_audacity import Send2Audacity
from bin.ui.nb_tad_editor import TadEditor
from bin.ui.nb_filemanager import FileManager
from bin.ui.nb_about import About
from bin.ui.nb_comp_and_render import CompAndRender
from bin.ui.nb_settitle import SetTitle
from bin.ui.nb_settings import Settings

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
        self.title(f'LPRT - {VERSION}:{HASH}')
        self.geometry('1024x768')
        self.build_ui()
        WELCOME.destroy()
        
        AI = AsciiImage(IMG_LOGO)
    
        self.wm_iconphoto(False,AI.image)
    
    def get_ui_names(self) -> list[str]:
        """ Gets all ui_names """
        return [
            'Main',
            'Recording',
            'ThumbnailGenerate',
            'FetchAudio',
            'FixAudio',
            'Send2Audacity',
            'CompAndRender',
            'SetTitle',
            'Deploy',
            'TadEditor',
            'FileManager',
            'Settings',
            'About'
        ]
    
    def build_ui(self):
        """
        For each ui_element this prints you a message & create the desired element
        """
        ELEMENTS = [
            (Main, 'Main'),
            (Recording, 'Recording'),
            (ThumbnailGenerate,'ThumbnailGenerate'),
            (FetchAudio,'FetchAudio'),
            (FixAudio,'FixAudio'),
            (Send2Audacity,'Send2Audacity'),
            (CompAndRender,'CompAndRender'),
            (SetTitle,'SetTitle'),
            (Deploy,'Deploy'),
            (TadEditor,'TadEditor'),
            (FileManager,'FileManager'),
            (Settings,'Settings'),
            (About, 'About')
        ]
        for ui,name in ELEMENTS:
            LOG('Create: $',[name])
            ui(self.menu.get_root_for(name))