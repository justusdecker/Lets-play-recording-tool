VERSION = '<NULL>'
HASH = '<NULL>'
import tkinter as tk

from src.api.b64img import b642img
from src.api.icons import IMG_LOGO
from src.api.log import LOG

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
     
        self.title(f'LPRT')
        self.geometry('1024x768')
        
        self.MENU = tk.Menu(self)
        self.config(menu = self.MENU)
        
        self.MSUB_lprt = tk.Menu(self.MENU, tearoff=0)
        self.MENU.add_cascade(label="LPRT", menu = self.MSUB_lprt)
        self.MSUB_lprt.add_command(label="Quit", command = lambda: print("Quit"))
        self.MSUB_lprt.add_command(label="Settings", command = lambda: print("Settings"))
        
        
        self.MSUB_pages = tk.Menu(self.MENU, tearoff=0)
        self.MENU.add_cascade(label="Pages", menu = self.MSUB_pages)
        
        #! Create these button on start automatically by using a list from module
        self.MSUB_pages.add_command(label="Recording", command = lambda: print("Recording"))
        self.MSUB_pages.add_command(label="FetchAudio", command = lambda: print("FetchAudio"))
        
        #* Pages: User Automations
        #* Database related: Export, import etc.
        #* Filesystem related: Data Detection, Create Lets Play, Backup etc.
        #* Settings related
        #* About: Help, License etc.
        
    
        self.wm_iconphoto(False,b642img(IMG_LOGO))
    
    def read_custom_ui(self):
        ...
    
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
            'UploadAtSet',
            'Deploy',
            'TadEditor',
            'FileManager',
            'Settings',
            'About',
            'Help'
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
            (UploadAtSet,'UploadAtSet'),
            (Deploy,'Deploy'),
            (TadEditor,'TadEditor'),
            (FileManager,'FileManager'),
            (Settings,'Settings'),
            (About, 'About'),
            (Help, 'Help')
        ]
        for ui,name in ELEMENTS:
            LOG('Create: $',[name])
            ui(self.MENU.get_root_for(name))