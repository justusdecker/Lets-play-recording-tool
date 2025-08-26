"""
This Modules packs the compiled EXE & some other files into a zipfile
"""

import zipfile
from os import chdir
chdir('..')

with open('bin\\version.py') as f:
    VERSION = f.read().split(' = ')[1].replace("\'",'')
chdir('tools\\')
with zipfile.ZipFile(f'lprt_{VERSION}.zip','w') as ZIP:
    ZIP.write('dist\\main.exe','lprt.exe')
    ZIP.write('libpng16-16.dll','libpng16-16.dll')