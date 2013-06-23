class A:
    def __init__(self):
        self.A_data = None

class B:
    def __init__(self):
        self.B_data = None

def foo(*args):
    args[0].A_data = 1
    args[1].B_data = 3.14

a = A()
b = B()
foo(a, b)
x = a.A_data
print x
y = b.B_data
print y
