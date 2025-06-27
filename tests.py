class Tests:
    
    def __init__(self,meat: list):
        self.all_tests = [i for i in dir(meat) if i.startswith('test')]
        self.ok_tests = []
        
    def add(self,function_title: str):
        self.ok_tests.append(function_title)


def test_T():pass
def test_3(): pass
def lol(): pass
test = test_T()

TESTS = Tests(__all__)
print(__spec__)
print(TESTS.all_tests)