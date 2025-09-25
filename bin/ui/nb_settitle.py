import tkinter as tk
import tkinter.ttk as ttk
from bin.xmsgbox import xwar
from bin.ui.lpep_picker import LPEPPicker
from bin.ui.ui_utils import change_states
from bin.data_access import SQLAccess, AsciiImage, isfile
from threading import Thread
from bin.player_video import NewVideoPlayer
from bin.api.gemini_api import send_gemini, os
from bin.constants import ICO_UPNDOWN

class SetTitle(tk.Frame):
    """
    Displays information about the application, including its license.

    Provides a scrollable text area to show the full license text.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        W =tk.Frame(parent)
        
        self.menu = parent.master
        
        
        AUTOMATION_ROOT = ttk.Frame(W)

        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        self.lpep_picker = LPEPPicker(AUTOMATION_ROOT,self.run,'lp-ep')

        AUTOMATION_ROOT.pack()
        
        self.media_player = NewVideoPlayer(W, [],0,self)
        self.media_player.pack()
        
        
        gemini_stuff = ttk.LabelFrame(W,text='Ask Gemini for a hint')
        ttk.Label(gemini_stuff,text='Only input keywords! e.g. Gaming, Mining...').pack()
        self.v_t = tk.StringVar()
        self.gemini_entry = ttk.Entry(gemini_stuff,textvariable=self.v_t)
        img = AsciiImage(ICO_UPNDOWN)
        self.send_btn = ttk.Button(gemini_stuff,image=img.image,command=self.send_and_receive)
        self.send_btn.image = img.image
        self.gemini_entry.pack(fill=tk.X)
        self.send_btn.pack()
        
        scrollbar = ttk.Scrollbar(gemini_stuff,orient='vertical')
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.text = tk.Text(gemini_stuff, width = 80, height = 5, wrap = tk.NONE,
                 yscrollcommand = scrollbar.set)
        
        
        self.text.pack(fill=tk.X)
        scrollbar.config(command=self.text.yview)
        
        gemini_stuff.pack()
        
        W.pack()
    
    def update_text(self, text):
        """ Cleans up the text & rewrites it with the given `text` variable """
        self.text.delete('1.0',tk.END)
        for i in text.splitlines():
            self.text.insert(tk.END, f'{i}\n')
            
    def run(self,*args):
        
        a, b = int(self.lpep_picker.v_epstart.get())-1, int(self.lpep_picker.v_epend.get())
        lpid = SQLAccess.read_letsplay_by_option_var(self)
        data = [i + 1 for i in range(a,b+(1 if a == b else 0))]
        for i in data:
            vp = SQLAccess.read_final_video_path(lpid,i-1)
            if vp is None: 
                xwar('Failed loading\nDatabase entry is NULL.')
                return
            if not isfile(vp):
                xwar(f'Failed loading\nFile:{vp} does not exist.')
                return
        
        self.media_player.reset(data, lpid)
    
    def send_and_receive(self,*args):
        """ Runs a thread that targets `self.__sar` """
        change_states([self.gemini_entry, self.send_btn],'disabled')
        Thread(target=self.__sar).start()
    
    def __sar(self):
        """ This sends data to gemini & updates the tk.Text Widget with the result """
        __lang: str | None = os.getenv("LANG")
        self.update_text(str(send_gemini(f'Please answer me in [{__lang}]. Generate me a youtube title(gaming / lets play) in the language=[\"{__lang}\"] for: {self.v_t.get()}')))
        change_states([self.gemini_entry, self.send_btn],'!disabled')
