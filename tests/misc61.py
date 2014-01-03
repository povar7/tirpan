import random

class A(object):
    pass

class B(object):
    pass

if random.randint(0, 1):
    x = A()
else:
    x = B()

print x.foo
