from TestSuit import TestSuite

# This is used to test the TestSuit class
expectedOutput = 6


def add(a, b, c):
    return a + b + c

testcase = TestSuite("adding numbers")
testcase.test(add, 6, 1, 2, 3)


# Testsuit works