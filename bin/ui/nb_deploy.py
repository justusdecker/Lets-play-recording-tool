from bin.ui.automation_frame import AutomationFrame
from bin.auto.wf_deploy import DeployWF
import tkinter.ttk as ttk
import tkinter as tk

class Deploy(AutomationFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.automation_callback = DeployWF
        
        self.dtf_enabled = tk.BooleanVar(value=False)
        self.mfp_enabled = tk.BooleanVar(value=False)
        self.cof_enabled = tk.BooleanVar(value=False)
        
        options_frame = ttk.Frame(self.AUTOMATION_ROOT)
        options_frame.pack(pady=10,)
        
        dtf_frame = ttk.LabelFrame(options_frame, text='Delete temp files')
        dtf_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Checkbutton(dtf_frame, text='Activate', variable=self.dtf_enabled).grid(row=0, column=0, sticky='w')
        
        mfp_frame = ttk.LabelFrame(options_frame, text='Move files to another path')
        mfp_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Checkbutton(mfp_frame, text='Activate', variable=self.mfp_enabled).grid(row=0, column=0, sticky='w')
        
        cof_frame = ttk.LabelFrame(options_frame, text='clear the output folder')
        cof_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Checkbutton(cof_frame, text='Activate', variable=self.cof_enabled).grid(row=0, column=0, sticky='w')
        
        options_frame.pack()
        dtf_frame.pack()
        mfp_frame.pack()
        cof_frame.pack()