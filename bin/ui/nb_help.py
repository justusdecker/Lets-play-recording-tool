from bin.welcome_popup import WELCOME
from bin.translation import gtran
import tkinter as tk
import tkinter.ttk as ttk
from bin.constants import HELP, ROOT
from bin.data_access import file_write
from os import system

HELPFILEPATH = f'{ROOT}help.html'

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

        ttk.Button(W,text='Show Help',command=self.gen_html).pack()
        
        W.pack(expand = True, fill = tk.BOTH)
    def gen_html(self, *_):
        file_write(HELPFILEPATH, HELP)
        system(f'start {HELPFILEPATH}')