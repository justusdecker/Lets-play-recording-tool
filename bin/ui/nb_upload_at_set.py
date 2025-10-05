from bin.ui.automation_frame import AutomationFrame
from bin.auto.wf_upload_at_set import UploadAtSetWF
from tkcalendar import Calendar
import tkinter.ttk as ttk
import tkinter as tk

HOURS = [f'{i:02d}' for i in range(24)]
MINUTES = [f'{i:02d}' for i in range(0,60,15)]

class UploadAtSet(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = UploadAtSetWF
        
        LF1 = ttk.LabelFrame(self.AUTOMATION_ROOT,text='Date')
        
        self.date = Calendar(LF1, selectmode= 'day')
        self.date.pack()
        
        LF2 = ttk.LabelFrame(self.AUTOMATION_ROOT,text='Time')
        
        self.hour = tk.StringVar()
        
        hcb = ttk.Combobox(LF2,
                     width=5,
                     textvariable=self.hour)
        
        self.minutes = tk.StringVar()
        
        mcb = ttk.Combobox(LF2,
                     width=5,
                     textvariable=self.minutes)
        
        hcb['values'] = HOURS
        hcb.pack(side='left')
        
        mcb['values'] = MINUTES
        mcb.pack(side='left')
        
        
        LF1.pack()
        LF2.pack()