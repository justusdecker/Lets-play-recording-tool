from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

from tkinter import Frame, X
from tkinter.ttk import Label
from tkinter.messagebox import showerror

try: #Fix for issue: #127
    from PIL import ImageTk, Image
except:
    from bin.constants import ERROR_008
    showerror('ERROR', ERROR_008 + '\nPIL')
    quit()

class ThumbnailPreview(Frame):
    """
    A Toplevel window for displaying a thumbnail preview.

    This window shows an image, typically a thumbnail, updates its title
    and displayed image based on the provided path and index.
    """
    def __init__(self,parent):
        super().__init__()
        
        self.label = Label(parent)
        self.label.pack(pady=20)
        self.update_image(f'bin\\data\\img\\logo.ico',-1)

    def update_image(self,path: str,i:int | None):
        """
        Updates the displayed image and the window title.

        Resizes the image from the given path and displays it on the label.
        The window title is updated to reflect the episode number or "TADEditor" in case of using this with the TADEditor.

        Args:
            path (str): The file path to the image to be displayed.
            i (int | None): An optional index for the image, used in the window title.
                            If None, "TADEditor" is used in the title.
        """
        f'Thumbnail Preview: {i+1 if i is not None else "TADEditor"}' #! Title set currently not avaiable
        self.image = Image.open(path).resize((512,288))
        self.image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.image,border=2,relief="raised")
   