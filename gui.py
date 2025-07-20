"""
from tkinter import Tk
import tkinter
import tkinter.ttk
tkinter.HIDDEN
T = Tk('Test')
MENU = tkinter.ttk.Frame(T)
for i in range(5):
    btn = tkinter.ttk.Button(MENU,text = f'{i}')
    btn.grid(column=1)
frame = tkinter.ttk.Frame(T)
    
btn = tkinter.ttk.Button(T,text = 'Some functionality here!')


btn.grid(column=2,row=0)

#slr = tkinter.ttk.LabeledScale(frame)
#slr.grid(column=3,row=0)

#nb = tkinter.ttk.Label(frame)
#nb.grid(column=4,row=0)

#slr = tkinter.ttk.LabeledScale(frame,)
#slr.grid()

MENU.grid(column=1,row=0)
frame.grid(column=2)

T.mainloop()
# MENU LEFT
# FRAME RIGHT
"""

import tkinter as tk
from tkinter import ttk

LARGEFONT =("Verdana", 35)

class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        # initializing frames to an empty array
        self.frames = {}
        
        for F in (StartPage, Page1, Page2):
 
            frame = F(container, self)
            
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
 
def get_menu(parent,controller) -> ttk.Frame:
    
    MENU = ttk.Frame(parent)

    button1 = ttk.Button(MENU, text ="Page 1", command = lambda : controller.show_frame(Page1))

    button1.grid(row = 0, column = 0, padx = 10)

    button2 = ttk.Button(MENU, text ="Page 2",command = lambda : controller.show_frame(Page2))

    button2.grid(row = 1, column = 0, padx = 10)
    
    MENU.grid(column=0,row=0)
    
class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        # label of frame Layout 2
        label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
        
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 1, padx = 10, pady = 10) 
 
 
        MENU = get_menu(self, controller)
        
 
         
 
 
# second window frame page1 
class Page1(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
 
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
    
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
 
        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text ="Page 2",
                            command = lambda : controller.show_frame(Page2))
    
        # putting the button in its place by 
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
 
 
 
 
# third window frame page2
class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
 
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Page 1",
                            command = lambda : controller.show_frame(Page1))
    
        # putting the button in its place by 
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
 
        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
    
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
 
 
# Driver Code
app = TkinterApp()
app.mainloop()


