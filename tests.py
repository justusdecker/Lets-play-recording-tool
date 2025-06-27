from bin.data_access import file_write, file_append
class Tests:
    
    def __init__(self,meat):
        self.all_tests = [i for i in dir(meat) if i.startswith('test')]
        self.ok_tests = []
        
    def add(self,function_title: str):
        self.ok_tests.append(function_title)
        
    def write(self):
        file_write('testing.md','')
        for test in self.all_tests:
            if test in self.ok_tests:
                file_append('testing.md',f'> SUCCESS\n> {test}')
            else:
                file_append('testing.md',f'> [!CAUTION]\n> {test}')