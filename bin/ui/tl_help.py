import tkinter as tk
from tkinter import ttk, scrolledtext

def create_help_page(
    title:str, 
    text: str,
    geometry: str = '600x400'):
    
    """
    Creates a new Toplevel window (help page) with a title and scrollable text content.

    This function is typically used to display help text, information, or
    longer messages in a separate, non-modal view. The text content
    is inserted in a read-only state.

    """
    
    window = tk.Toplevel()
    window.title(title)
    window.geometry(geometry)
    
    main_frame = ttk.Frame(window, padding = 10)
    main_frame.pack(expand = True, fill = tk.BOTH)
    
    helptext_widget = scrolledtext.ScrolledText(
        main_frame,
        wrap= tk.WORD,
        width = 60,
        height = 20,
        font = ('Arial', 10),
        padx = 5,
        pady = 5)
    
    helptext_widget.pack(expand = True, fill = tk.BOTH)
    
    helptext_widget.insert(tk.INSERT, text)
    helptext_widget.config(state = tk.DISABLED)

create_help_page('Hello World', 'We will test some cases!\ngrg')