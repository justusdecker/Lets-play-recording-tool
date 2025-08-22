from bin.dlls import LIBPNG16_16DLL
from os.path import isfile
def create_libpng16_16_ine():
    if not isfile('libpng16-16.dll'):
        with open('libpng16-16.dll','wb') as fo:
            fo.write(LIBPNG16_16DLL)