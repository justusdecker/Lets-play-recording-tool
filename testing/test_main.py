from bin.welcome_popup import WELCOME
from bin.translation import gtran
WELCOME.update_message(f'{gtran("bin::welcome::load")} {__name__}')
from bin.data_access import on_start
from bin.ui.tkinter_app import TkinterApp
from bin.api.dll_loader import create_libpng16_16_ine

if __name__ == '__main__':
    create_libpng16_16_ine()
    on_start()
    from bin.translation import gtran
    WELCOME.update_message(gtran("bin::welcome::create_app"))
    APP = TkinterApp()
    APP.mainloop()
     
    
