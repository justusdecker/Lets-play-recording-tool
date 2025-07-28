

from tkinter import (
    Toplevel
)
from tkinter.ttk import (
    Label
)

from tkinter.messagebox import showerror

try: #Fix for issue: #127
    from PIL import ImageTk, Image
except:
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nPIL')
    quit()

class ThumbnailPreview(Toplevel):
    def __init__(self):
        super().__init__()
        self.isfinished = False
        self.geometry('640x400')
        self.label = Label(self)
        self.label.pack(pady=20)
        
        self.update_image(f'bin\\data\\img\\logo.ico',-1)
        
        
    def update_image(self,path: str,i:int):
        self.title(f'Thumbnail Preview: {i+1}')
        self.image = Image.open(path).resize((640,360))
        self.image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.image,border=2,relief="raised")
        
    def byebye(self, *args):
        """Closes the ThumbnailPreview window."""
        self.destroy()
   