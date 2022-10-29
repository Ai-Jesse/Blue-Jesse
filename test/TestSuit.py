class TestSuite:
    def __init__(self, name):
        self.name = name # the name of the test
        return 
    def test(self, testmethod, expectedOutput, *inputData):
        try:
            print(*inputData)
            assert testmethod(*inputData) == expectedOutput
            print("Test " + str(self.name) + " passed successfuly")
        except:
            print("You have bad code")
            print(str(*inputData) + " does not equal to " + str(expectedOutput))

            