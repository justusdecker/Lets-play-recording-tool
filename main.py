
from bin.constants import *
from bin.obs import OBSObserver
from bin.data_access import LetsPlay, file_read, isfile, LP_KEYS, file_write
from tkinter.filedialog import asksaveasfilename as asafn
class App:
    def __init__(self):
        self.isrunning = True
        self.current_letsplay_id = 0
    def main_menu(self):
        """
        Main Menu >
        """
        user_input = input()
        if not user_input.isdecimal():
            return
        match int(user_input):
            case 1:
                # OBS - Recording
                # Will save your recording data to the in lets_play.csv referrenced episode file
                OBSO = OBSObserver()
                if not OBSO.isconnected:
                    print('No connection to OBS!')
                while OBSO.isconnected:
                    try:
                        print(OBSO.timecode)
                    except KeyboardInterrupt:
                        break
                print('No connection to OBS!')
                    
            case 2:
                self.automation_sub_menu()
            case 5:
                self.data_sub_menu()
            case 0:
                self.isrunning = False
            case _:
                print(USER_INPUT_NUM_UNMATCHED)
    def data_sub_menu(self):
        
        print(MENU_DATA_MESSAGE)
        user_input = input()
        if not user_input.isdecimal():
            err('Input must be an integer')
            return
        match int(user_input):
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
            print(MENU_DATA_DELETE_MESSAGE)
            user_input = input()
            if not user_input.isdecimal():
                continue
            match int(user_input):
                case 0:
                    return
                case _:
                    print(USER_INPUT_NUM_UNMATCHED)
    def data_sub_update_menu(self):
        while self.isrunning:
            print(MENU_DATA_UPDATE_MESSAGE)
            user_input = input()
            if not user_input.isdecimal():
                continue
            match int(user_input):
                case 0:
                    return
                case _:
                    print(USER_INPUT_NUM_UNMATCHED)
    def data_sub_read_menu(self):
        while self.isrunning:
            print(MENU_DATA_READ_MESSAGE)
            user_input = input()
            if not user_input.isdecimal():
                continue
            match int(user_input):
                case 0:
                    return
                case _:
                    print(USER_INPUT_NUM_UNMATCHED)
    def data_sub_create_file_menu(self):
        
        print(MENU_DATA_CREATE_FILE_MESSAGE)
        user_input = input()
        if not user_input.isdecimal():
            err('Input must be an integer')
            return
        match int(user_input):
            case 0:
                return
            case 1: # Create Lets Play.csv
                filepath = asafn(filetypes=[['CSV','*.csv']])
                if not isfile(filepath):
                    file_write(filepath,'')
                else:
                    err('File already exist!')
                return
            case _:
                print(USER_INPUT_NUM_UNMATCHED)
    def data_sub_create_entry_menu(self):
        while self.isrunning:
            print(MENU_DATA_CREATE_ENTRY_MESSAGE)
            user_input = input()
            if not user_input.isdecimal():
                continue
            match int(user_input):
                case 0:
                    return
                case _:
                    print(USER_INPUT_NUM_UNMATCHED)
    def automation_sub_menu(self):
        while self.isrunning:
            print(MENU_AUTOMATION_MESSAGE)
            user_input = input()
            if not user_input.isdecimal():
                continue
            match int(user_input):
                case 1:
                    pass
                case 5:
                    return
                case _:
                    print(USER_INPUT_NUM_UNMATCHED)
                    
        
    def loop(self):
        while self.isrunning:
            print(MENU_MESSAGE)
            self.main_menu()
            
if __name__ == "__main__":
    APP = App()
    APP.loop()