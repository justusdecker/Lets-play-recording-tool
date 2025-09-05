"""
This Modules packs the compiled EXE & some other files into a zipfile
"""

import zipfile
import os
print(os.getcwd())
VERSION = None
with open('./bin/version.py') as f:
    exec(f.read())

with zipfile.ZipFile(f'./tools/lprt_{VERSION}.zip','w') as ZIP:
    ZIP.write('./tools/dist/main.exe','lprt.exe')
    ZIP.write('./README.md','README.md')
    ZIP.write('./LICENSE','LICENSE')