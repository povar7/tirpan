import random

class A(object):
    def __init__(self, data):
        self.data = data

    def foo(self):
        print self.data

a = A(random.randint(0, 1))
a.foo()
