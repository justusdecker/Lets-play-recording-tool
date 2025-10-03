from bin.welcome_popup import WELCOME
from bin.translation import gtran


import tkinter as tk
import tkinter.ttk as ttk
from bin.constants import HELP_WORKFLOWS



class Help(tk.Frame):
    """
    Displays information about the application, including its license.

    Provides a scrollable text area to show the full license text.
    """
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        
        W = ttk.Frame(parent)
        

        WELCOME.update_message(f'Create Helppage')

        #! Help Here!

        W.pack(expand = True, fill = tk.BOTH)
