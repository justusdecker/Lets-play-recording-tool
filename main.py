from bin.welcome_popup import WELCOME
from bin.translation import gtran
WELCOME.update_message(f'{gtran("bin::welcome::load")} {__name__}')

from bin.xmsgbox import xqu
from bin.constants import VERSION, __LICENSE__
from bin.data_access import on_start
from os import system
from bin.download_file import send_heartbeat, get_newest_version_number
from bin.ui.tkinter_app import TkinterApp
from bin.api.dll_loader import create_libpng16_16_ine

from bin.ui.tl_help import create_help_page



def check_version():
    """
    Prompts the user a msgbox if the current version is not equal to the api version
    """
    if get_newest_version_number()['version'] != '_'.join(VERSION.split('.')[0:2]):
        if xqu('New Update avaiable\nDo you want to visit the update website?'):
            system('start https://github.com/justusdecker/Lets-play-recording-tool/releases')
from bin.constants import HELP_WORKFLOWS  
if __name__ == '__main__':
    create_libpng16_16_ine()
    on_start()
    send_heartbeat()
    from bin.translation import gtran
    WELCOME.update_message(gtran("bin::welcome::create_app"))
    APP = TkinterApp()
    check_version()
    create_help_page('Hello World', HELP_WORKFLOWS)
    APP.mainloop()
     
    
