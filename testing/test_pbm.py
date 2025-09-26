"""
Copy this file to ./root
"""
import tkinter as tk
import tkinter.ttk as ttk
from bin.ui.progress_bar_manager import ProgressBarManager

class DemoApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("AIO Progress Bar Demo (Clean)")
        self.pb_manager = ProgressBarManager(self, maximum=50, length=300)
        self.pb_manager.progress_bar.pack(pady=10)
        ttk.Button(self, text="Start Non-Blocking Task", command=self._start_task_callback).pack()
        ttk.Button(self, text="Reset Bar", command=self.pb_manager.reset_task).pack()
        
    def _start_task_callback(self):
        self.pb_manager.start_task(step_ms=100) 
if __name__ == '__main__':
    root = DemoApp()
    root.mainloop()
