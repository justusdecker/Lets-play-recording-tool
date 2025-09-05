"""
This converts images to ascii like strings
"""
import base64
from tkinter.filedialog import askopenfilename
from os.path import isfile
filepath: str = askopenfilename(filetypes=[('PNG Images','*.png')])
if not isfile(filepath):
    exit(1)
with open(filepath, 'rb') as f:
    base64string = base64.b64encode(f.read()).decode('ascii')
    with open('./tools/img.txt','w') as fo:
        fo.write(base64string)
print("Written b64str to: [./tools/img.txt]")