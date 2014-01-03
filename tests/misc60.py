import random

class A(object):
    pass

a = A()
setattr(a, 'data', random.randint(0, 1))
print a.data.__class__
