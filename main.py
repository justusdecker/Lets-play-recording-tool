
from bin.constants import MENU_MESSAGE, USER_INPUT_NUM_UNMATCHED, MENU_AUTOMATION_MESSAGE
from bin.obs import OBSObserver
class App:
    def __init__(self):
        self.isrunning = True
        
    def main_menu(self):
        match int(self.user_input):
            case 1:
                OBSO = OBSObserver()
                print(OBSO.timecode)
                while self.isrunning:
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
        
    def loop(self):
        while self.isrunning:
            print(MENU_MESSAGE)
            user_input = input()
            if not user_input.isdecimal():
                continue
            match int(user_input):
                case 1:
                    OBSO = OBSObserver()
                    print(OBSO.timecode)
                    while self.isrunning:
                        print(OBSO.timecode)
                case 2:
                    print(MENU_AUTOMATION_MESSAGE)
                case 5:
                    self.isrunning = False
                case _:
                    print(USER_INPUT_NUM_UNMATCHED)
            
if __name__ == "__main__":
    APP = App()
    APP.loop()