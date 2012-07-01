class A:
    pass

class B(A):
    x = 1
    y = 2
    def __init__(self, y):
        self.y = y

b = B(3)
print B.x
print b.x
print B.y
print b.y
