class A:
    pass

class B(A):
    x = 1
    y = 2.0
    def __init__(self, y, t):
        self.y = y
        self.t = t

a   = 3l
a   = 'abc'
b   = B(a, a)
print B.x
print b.x
print B.y
print b.y
print b.t
b.z = 4j
c   = b.z
print c
