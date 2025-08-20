from tkinter import ttk
import tkinter as tk

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
        self.menu = Notebook(self,['test','hello','world'])
        self.geometry('800x600')



if __name__ == '__main__':
    APP = TkinterApp()
    APP.mainloop()