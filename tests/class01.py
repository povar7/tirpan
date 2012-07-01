class A:
    pass

class B(A):
    x = 1

print B.x
print B.__bases__
