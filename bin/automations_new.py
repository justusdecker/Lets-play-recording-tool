from bin.obs import OBSObserver
from bin.data_access import *
from tkinter.ttk import Label

def obs_connect(ep: Episode,el):
    """
    Connects to the obs_ws API
    
    Runs until the connection breaks up or a keyboard interrupt happens
    """
    OBSO = OBSObserver()
    if OBSO.failed:
        el.btn_connect.configure(text= 'Settings File does not exist!')
        return
    if not OBSO.isconnected:
        el.btn_connect.configure(text= 'No Connection!')
        return
    while OBSO.isconnected:
        el.btn_connect.configure(text= 'Connection established')
        try:
            el.label.configure(text= OBSO.timecode)
            OBSO.update(ep)
        except:
            el.btn_connect.configure(text= 'Unexpected Error happened')
            print('Unexpected Error happened')