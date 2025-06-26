
from bin.constants import MENU_MESSAGE, USER_INPUT_NUM_UNMATCHED, MENU_AUTOMATION_MESSAGE
from bin.obs import OBSObserver
class App:
    def __init__(self):
        self.isrunning = True
        
    def main_menu(self):
        user_input = input()
        if not user_input.isdecimal():
            return
        match int(user_input):
            case 1:
                OBSO = OBSObserver()
                print(OBSO.timecode)
                while OBSO.isconnected:
                    print(OBSO.timecode)
            case 2:
                self.automation_sub_menu()
            case 5:
                self.isrunning = False
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