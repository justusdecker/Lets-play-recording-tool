"""
Move this file temporary into root & executing it will copy the `libpng16-16.dll` into `bin.dll_loader.py`
"""
with open('tools\\libpng16-16.dll','rb') as fi:
    data = fi.read()
with open('bin\\dll_loader.py','w') as fo:
    fo.write(f'LIBPNG16_16DLL = {data}')