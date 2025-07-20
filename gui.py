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

MENU_FORBIDDEN = False

DISCLAIMER = """
Welcome to LPRT

This Tool is currently Work in Progress!
Some features might not work as expected & can cause data loss! Be careful!
"""




class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        # initializing frames to an empty array
        self.frames = {}
        
        for F in (Main, Recording, ThumbnailGenerate, FetchAudio, FixAudio, Send2Audacity, CompAndRender, Settings):
 
            frame = F(container, self)
            
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(Main)
    def show_frame(self, cont):
        if not MENU_FORBIDDEN:
            frame = self.frames[cont]
            frame.tkraise()
        else:
            #! ERROR MSG to User
            pass
 
def get_menu(parent,controller) -> ttk.Frame:
    
    MENU = ttk.Frame(parent)
    
    OPTIONS = {'padx': 10, 'column': 0,'sticky':'W'}

    button1 = ttk.Button(MENU, text ="Main", command = lambda : controller.show_frame(Main))

    button1.grid(row = 0, **OPTIONS)

    button2 = ttk.Button(MENU, text ="Recording",command = lambda : controller.show_frame(Recording))

    button2.grid(row = 1, **OPTIONS)
    
    button3 = ttk.Button(MENU, text ="ThumbnailGenerate",command = lambda : controller.show_frame(ThumbnailGenerate))

    button3.grid(row = 2, **OPTIONS)
    
    button4 = ttk.Button(MENU, text ="FetchAudio",command = lambda : controller.show_frame(FetchAudio))

    button4.grid(row = 3, **OPTIONS)
    
    butto5 = ttk.Button(MENU, text ="FixAudio",command = lambda : controller.show_frame(FixAudio))

    butto5.grid(row = 4, **OPTIONS)
    
    button6 = ttk.Button(MENU, text ="Send2Audacity",command = lambda : controller.show_frame(Send2Audacity))

    button6.grid(row = 5, **OPTIONS)
    
    button7 = ttk.Button(MENU, text ="CompAndRender",command = lambda : controller.show_frame(CompAndRender))

    button7.grid(row = 6, **OPTIONS)
    
    button8 = ttk.Button(MENU, text ="Settings",command = lambda : controller.show_frame(Settings))

    button8.grid(row = 7, **OPTIONS)
    
    MENU.grid(column=0,row=0)
    
class Main(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text =DISCLAIMER)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        get_menu(self, controller)

class Recording(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="Recording", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        self.obs_running = False
        
        self.btn_connect = ttk.Button(self, text ="Connect to obs",command=self.get_connection)

        self.btn_connect.grid(row = 0, column=2)
        
        #TODO
        #! Connect & Disconnect OBS Button
        #! Show Time
        #! Show selected Lets Play
        #! Show current Episode
        
        get_menu(self, controller)
    def get_connection(self):
        self.obs_running = True
        
        self.btn_connect.state(["disabled"])
        print("Whatever")
        
        
class ThumbnailGenerate(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="ThumbnailGenerate", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        get_menu(self, controller)
class FetchAudio(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="FetchAudio", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        get_menu(self, controller)
        
class FixAudio(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="FixAudio", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        get_menu(self, controller)
class Send2Audacity(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="Send2Audacity", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        get_menu(self, controller)

class CompAndRender(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="CompAndRender", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        get_menu(self, controller)

class Settings(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text ="Settings", font = LARGEFONT)

        label.grid(row = 0, column = 1, padx = 10, pady = 10) 

        get_menu(self, controller)
app = TkinterApp()
app.mainloop()


