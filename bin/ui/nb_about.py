import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from bin.constants import __LICENSE__
class About(tk.Frame):
    """
    Displays information about the application, including its license.

    Provides a scrollable text area to show the full license text.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        
        # Create Headers
        LICENSE = ttk.LabelFrame(W,text='license')
        
        license_text = scrolledtext.ScrolledText(
            LICENSE,
            wrap= tk.WORD,
            width = 60,
            height = 20,
            font = ('Arial', 10),
            padx = 5,
            pady = 5)
        
        license_text.pack(expand = True, fill = tk.BOTH)
        
        
        license_text.insert(tk.INSERT, __LICENSE__)
        license_text.config(state = tk.DISABLED)
        
        LICENSE.pack(expand = True, fill = tk.BOTH)
        
        W.pack(expand = True, fill = tk.BOTH)
