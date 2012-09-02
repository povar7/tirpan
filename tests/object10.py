import sys

class A:
    def __init__(self, data):
        self.data = data

def foo(argparser):
    return argparser.data[0]

a = A(sys.argv)
x = foo(a)
print x

