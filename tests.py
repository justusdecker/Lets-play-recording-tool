class Tests:
    
    def __init__(self,meat):
        self.all_tests = [i for i in dir(meat) if i.startswith('test')]
        self.ok_tests = []
        
    def add(self,function_title: str):
        self.ok_tests.append(function_title)