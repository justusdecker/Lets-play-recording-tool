import testing.test_data_access, testing.test_obs

class Tests:
    def __init__(self):
        meat = dir(testing.test_data_access) + dir(testing.test_obs)
        self.all_tests = [i for i in meat if i.startswith('test')]
        self.ok_tests = []
    def add(self,function_title: str):
        self.ok_tests.append(function_title)

print(dir(testing.test_data_access))