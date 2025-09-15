from bin.welcome_popup import WELCOME
from bin.translation import gtran
WELCOME.update_message(f'{gtran("bin::welcome::load")} {__name__}')

import tkinter.messagebox as msgbox
from bin.constants import VERSION, __LICENSE__
from bin.data_access import on_start
from os import system
from bin.download_file import send_heartbeat, get_newest_version_number
from bin.ui.tkinter_app import TkinterApp
from bin.dll_loader import create_libpng16_16_ine

def check_version():
    """
    Prompts the user a msgbox if the current version is not equal to the api version
    """
    if get_newest_version_number()['version'] != '_'.join(VERSION.split('.')[0:2]):
        if msgbox.askyesno('New Update avaiable','Do you want to visit the update website?'):
            system('start https://github.com/justusdecker/Lets-play-recording-tool/releases')
            
if __name__ == '__main__':
    create_libpng16_16_ine()
    on_start()
    send_heartbeat()
    from bin.translation import gtran
    WELCOME.update_message(gtran("bin::welcome::create_app"))
    APP = TkinterApp()
    check_version()
    APP.mainloop()
     
    
