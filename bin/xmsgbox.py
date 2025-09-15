"""
This module provides simple wrapper functions for displaying Tkinter message boxes.

The functions are designed for convenience, offering quick ways to show
warning, error, and info message boxes with a standardized title.
"""

import tkinter.messagebox as msgbox

def xwar(msg: str) -> None:
    """Displays a Tkinter warning message box."""
    msgbox.showwarning('Warning', msg)
def xerr(msg: str) -> None:
    """Displays a Tkinter error message box."""
    msgbox.showerror('Error', msg)
def xinf(msg: str) -> None:
    """Displays a Tkinter information message box."""
    msgbox.showinfo('Info', msg)