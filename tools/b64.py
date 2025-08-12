"""
This converts images to ascii like strings
"""

import base64
from PIL import ImageTk, Image
from io import BytesIO

with open('bin\\data\\img\\ui\\run.png', 'rb') as f:
    print(len(f.read()))
    base64string = base64.b64encode(f.read()).decode('ascii')
    
    
    with open('tools\\img.txt','w') as fo:
        fo.write(base64string)
print(base64string)


from os import mkdir, remove

from tkinter import PhotoImage

class AsciiImage:
    def __init__(self, var: str):
        self.var = var

        io = BytesIO(base64.b64decode(var.encode('ascii')))
        img = Image.open(io)
        self.image = ImageTk.PhotoImage(img)
