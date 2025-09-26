import tkinter as tk
import tkinter.ttk as ttk
from bin.ui.lpep_picker import LPEPPicker
class TKFrameWithLPControls(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.menu = parent.master
        
        W = tk.Frame(parent)
        
        AUTOMATION_ROOT = ttk.Frame(W)

        self.AUTOMATION_ROOT = AUTOMATION_ROOT
        
        self.lpep_picker = LPEPPicker(AUTOMATION_ROOT,self.run,'lp-ep')

        AUTOMATION_ROOT.pack()
        W.pack()
        self.W = W