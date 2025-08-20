from tkinter import ttk
import tkinter as tk
from tkinter.font import Font
from bin.constants import __LICENSE__, DISCLAIMER

class Notebook:
    def __init__(self, 
                 parent: tk.Tk | tk.Widget,
                 ui: list[str]):
        self.parent = parent
        
        self.notebook = ttk.Notebook(self.parent)
        
        self.frames = []
        self.names = ui.copy()
        
        for i in range(len(ui)):
            
            f = ttk.Frame(self.notebook)
            f.pack(padx=5,pady=5)
            self.notebook.add(f,text=self.names[i])
            self.frames.append(f)
        self.notebook.pack(padx=5,pady=5)
            
    def get_root_for(self,name: str):
        if not name in self.names: raise NameError
        return self.frames[self.names.index(name)]
        
        
        
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
        self.geometry('800x600')
        self.build_ui()
    def get_ui_names(self) -> list[str]:
        return [
            'Main',
            'Recording',
            'About'
        ]
    def build_ui(self):
        ELEMENTS = [
            (Main, 'Main'),
            (About, 'About')
        ]
        for ui,name in ELEMENTS:
            ui(self.menu.get_root_for(name))



class Main(tk.Frame):
    """
    Represents the main start page of the application.

    This frame serves as the initial view for the application,
    displaying a welcome message and a disclaimer, and integrating the
    navigation menu for other application pages.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        
        # Create Headers
        MAIN = ttk.LabelFrame(W,text='Welcome')
        
        label = ttk.Label(MAIN, text =DISCLAIMER)

        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Packing
        MAIN.pack()

        W.pack()

class About(tk.Frame):
    """
    Displays information about the application, including its license.

    Provides a scrollable text area to show the full license text.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        
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
        
        W.pack()


if __name__ == '__main__':
    APP = TkinterApp()
    APP.mainloop()