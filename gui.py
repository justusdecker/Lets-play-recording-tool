from tkinter import Tk
import tkinter
import tkinter.ttk

T = Tk('Test')
for i in range(5):
    btn = tkinter.ttk.Button(T,text = 'Im a Button')
    btn.grid(column=1)
btn = tkinter.ttk.Button(T,text = 'Im a Button')
btn.grid(column=2,row=0)

slr = tkinter.ttk.LabeledScale(T)
slr.grid(column=3,row=0)

nb = tkinter.ttk.Label(T,)
nb.grid(column=4,row=0)

slr = tkinter.ttk.LabeledScale(nb)
slr.grid()

T.mainloop()