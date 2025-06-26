

class App:
    def __init__(self):
        self.user_input = ""
    
    @property
    def args(self) -> list[str]:
        return self.user_input.split(' ')
    
    def loop(self):
        while self.isrunning:
            self.user_input = input()