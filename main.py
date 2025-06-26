
from bin.constants import MENU_MESSAGE
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
            
            
if __name__ == "__main__":
    APP = App()
    APP.loop()