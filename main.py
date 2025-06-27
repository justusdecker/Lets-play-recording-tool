
from bin.constants import *
from bin.obs import OBSObserver
from bin.data_access import LetsPlay, file_read, isfile, LP_KEYS, file_write,csv_write
from tkinter.filedialog import asksaveasfilename as asafn
from bin.others import binpi
LP_PATH = 'lets_plays.csv'
def obs_connect():
    OBSO = OBSObserver()
    if not OBSO.isconnected:
        err('No connection to OBS!')
    while OBSO.isconnected:
        try:
            print(OBSO.timecode)
        except KeyboardInterrupt:
            err('Keyboard interrupt!')
            break

def create_new_lp_file():
    print(color816(f'[!TIP] > If you have a typo somewhere: You can change the data later manually!(Do it or bugs will kill your fun :D)',32))
    if not isfile(LP_PATH):
        csv_write(LP_PATH,[[binpi(f'{key}: ') if key != 'version' else file_read('version.txt') for key in LP_KEYS]])
    else:
        err('File already exist!')
    pass

class App:
    def __init__(self):
        self.isrunning = True
        self.current_letsplay_id = 0
        if not isfile('lets_play.csv'):
            war('lets_play.csv does not exist & will be created!')
            create_new_lp_file()
    def main_menu(self):
        """
        Main Menu >
        """
        match binpi(MENU_MESSAGE):
            case 1:
                # OBS - Recording
                # Will save your recording data to the in lets_play.csv referrenced episode file
                obs_connect()
                    
            case 2:
                self.automation_sub_menu()
            case 4:
                self.data_sub_menu()
            case 5:
                binpi('Set the lets play id') #! 
            case 0:
                self.isrunning = False
            case _:
                err(USER_INPUT_NUM_UNMATCHED)
   
    def data_sub_menu(self):
        """
        Main > Data >
        
        This method redirects to other methods, returns if user wants to go back or print an error msg
        """
        while self.isrunning:
            
            match binpi(MENU_DATA_MESSAGE):
                case 1:
                    self.data_sub_create_file_menu()
                case 2:
                    self.data_sub_create_entry_menu()
                case 3:
                    self.data_sub_read_menu()
                case 4:
                    self.data_sub_update_menu()
                case 5:
                    self.data_sub_delete_menu()
                case 0:
                    return
                case _:
                    err(USER_INPUT_NUM_UNMATCHED)
    
    def data_sub_delete_menu(self):
        while self.isrunning:

            match binpi(data_sub_menu('Delete')):
                case 0:
                    return
                case _:
                    err(USER_INPUT_NUM_UNMATCHED)
    def data_sub_update_menu(self):
        while self.isrunning:
            
            match binpi(data_sub_menu('Update')):
                case 0:
                    return
                case _:
                    err(USER_INPUT_NUM_UNMATCHED)
    def data_sub_read_menu(self):
        while self.isrunning:
            
            match binpi(data_sub_menu('Read')):
                case 0:
                    return
                case _:
                    err(USER_INPUT_NUM_UNMATCHED)
    
    def data_sub_create_file_menu(self):
        while self.isrunning:

            match binpi(data_sub_menu('Create file')):
                case 0:
                    return
                case 1: # Create Lets Play.csv
                    create_new_lp_file()
                case _:
                    err(USER_INPUT_NUM_UNMATCHED)
    def data_sub_create_entry_menu(self):
        while self.isrunning:
            
            match binpi(data_sub_menu('Create entry')):
                case 0:
                    return
                case _:
                    err(USER_INPUT_NUM_UNMATCHED)
    def automation_sub_menu(self):
        while self.isrunning:

            match binpi(MENU_AUTOMATION_MESSAGE):
                case 1:
                    pass
                case 5:
                    return
                case _:
                    err(USER_INPUT_NUM_UNMATCHED)
                    
        
    def loop(self):
        while self.isrunning:
            self.main_menu()
            
if __name__ == "__main__":
    APP = App()
    APP.loop()