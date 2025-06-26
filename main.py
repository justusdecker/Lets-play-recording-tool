
from bin.constants import MENU_MESSAGE, USER_INPUT_NUM_UNMATCHED, MENU_AUTOMATION_MESSAGE
from bin.obs import OBSObserver
class App:
    def __init__(self):
        self.user_input = ""
        self.isrunning = True
    @property
    def args(self) -> list[str]:
        return self.user_input.split(' ')
    
    def loop(self):
        while self.isrunning:
            print(MENU_MESSAGE)
            self.user_input = input()
            if not self.user_input.isdecimal():
                continue
            match int(self.user_input):
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