from bin.welcome_popup import WELCOME
WELCOME.update_message(f'Load: {__name__}')

import tkinter.messagebox as msgbox
from bin.constants import VERSION, __LICENSE__
from bin.data_access import on_start
from os import system
from bin.download_file import send_heartbeat, get_newest_version_number
from bin.ui import TkinterApp

def check_version():
    if get_newest_version_number()['version'] != '_'.join(VERSION.split('.')[0:2]):
        if msgbox.askyesno('New Update avaiable','Do you want to visit the update website?'):
            system('start https://github.com/justusdecker/Lets-play-recording-tool/releases')

if __name__ == '__main__':
    on_start()
    send_heartbeat()
    WELCOME.update_message('Create App')
    APP = TkinterApp()
    check_version()
    APP.mainloop()
    
    
