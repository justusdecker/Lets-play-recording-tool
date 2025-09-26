import tkinter as tk
import tkinter.ttk as ttk
from collections.abc import Callable

class ProgressBarManager:
    """
    Manages a ttk.Progressbar instance for use in non-blocking/event-driven 
    environments (e.g., when a slow operation runs in the background or another thread).
    
    The UI update methods (set_progress, increment) are thread-safe if called
    via a mechanism that executes them on the main thread (like asyncio.to_thread 
    or the 'after' loop for simulation).
    """
    def __init__(self, parent: tk.Widget, maximum: int = 100, length: int = 200):
        self.parent = parent
        self.value_var = tk.DoubleVar(parent, value=0.0)
        self.progress_bar = ttk.Progressbar(
            parent,
            orient='horizontal',
            mode='determinate',
            length=length,
            variable=self.value_var,
            maximum=maximum
        )
        self.progress_bar.pack_forget() # Hidden by default

        self.clean(maximum)
        
    def clean(self,maximum: int = 100):
        self.current_step = 0
        self.total_steps = maximum
        self.after_id = None
        self.running = False
        self.maximum = float(maximum)
        self.progress_bar.configure(maximum=maximum)

    def start_task(self, step_ms: int = 50, callback_function: Callable | None = None):
        """ Starts the none-blocking Progresssimulation """
        if self.running: return 
        self.reset_task(reset_bar_only=True) # Resets counter & flags
        self.running = True
        self.step_ms = step_ms
        self.callback_function = callback_function
        self._simulate_progress()
        
    def _simulate_progress(self):
        """ 
        Internal Method, this will simulate progress & manage the AIO-Chain
        """
        if not self.running: return 
            
        if self.current_step < self.total_steps:
            self.current_step += 1
            self.increment(1)
            if self.callback_function: self.callback_function()
            self.after_id = self.parent.after(self.step_ms, self._simulate_progress)
        else:
            self.reset_task()
    
    def reset_task(self, reset_bar_only: bool = False):
        """ 
        Cancels the running Task-chain
        """
        self.running = False 
        
        if self.after_id is not None:
            try:
                self.parent.after_cancel(self.after_id)
            except ValueError:
                 pass 
            self.after_id = None
            
        self.current_step = 0
        if not reset_bar_only:
            self.reset()

    def set_progress(self, value: float):
        """
        Sets the progress bar to a specific value. Prevents overflow above self.maximum
        Must be called from the main (Tkinter) thread.
        """
        if value > self.maximum:
            value = self.maximum
        elif value < 0:
            value = 0
            
        self.value_var.set(value)

        if value > 0 and not self.progress_bar.winfo_ismapped():
            self.progress_bar.pack(padx=5)
    
    def set_max(self,val: float):
        self.maximum = val
    
    def increment(self, step: float = 1.0):
        """
        Increments the progress bar by a specific step. Prevents overflow.
        """
        current_value = self.value_var.get()
        new_value = current_value + step
        self.set_progress(new_value)
        print(new_value, self.maximum)

    def inc_max(self):
        """
        Forces the progress bar to its maximum value (100%) and terminates the task.
        This is used when a process finishes early or must visually complete.
        """
        self.set_progress(self.maximum)
        self.reset_task()
    
    def reset(self):
        """
        Resets the progress bar value to 0 and hides the widget.
        """
        self.value_var.set(0.0)
        if self.progress_bar.winfo_ismapped():
            self.progress_bar.pack_forget()

    def get_widget(self) -> ttk.Progressbar:
        """ Returns the Progressbar widget. """
        return self.progress_bar