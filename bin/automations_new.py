from bin.obs import OBSObserver
from bin.data_access import *
from tkinter.ttk import Label

def obs_connect(ep: Episode,el: Label):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up or a keyboard interrupt happens
    """
    OBSO = OBSObserver()
    if OBSO.failed:
        print('Settings File must exist!')
        return
    if not OBSO.isconnected:
        print('no cn')
        return
    while OBSO.isconnected:
        try:
            el.configure(text= OBSO.timecode)
            OBSO.update(ep)
        except KeyboardInterrupt:
            print('kbi')
            break
        except:
            print('Unexpected Error happened')