class B(type):
    def __init__(cls, name, bases, namespace):
        cls.foo = 1

class A(object):
    __metaclass__ = B

a = A()
print a.foo
