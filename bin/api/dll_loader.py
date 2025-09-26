from bin.api.dlls import LIBPNG16_16DLL
from os.path import isfile
def create_libpng16_16_ine():
    """ creates libpng16-16.dll if not exist """
    if not isfile('libpng16-16.dll'):
        with open('libpng16-16.dll','wb') as fo:
            fo.write(LIBPNG16_16DLL)