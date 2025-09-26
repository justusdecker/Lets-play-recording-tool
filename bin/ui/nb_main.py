import tkinter as tk
import tkinter.ttk as ttk
from bin.translation import gtran
from bin.constants import DISCLAIMER

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
        MAIN = ttk.LabelFrame(W,text=gtran("bin::ui::main_welcome_header"))
        
        label = ttk.Label(MAIN, text =DISCLAIMER)

        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        # Packing
        MAIN.pack()

        W.pack()