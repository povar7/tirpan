def foo(a, b):
    return (a, b)

def bar(n):
    return lambda x: foo(x, n)

tmp = bar(1)
y = tmp(3.14)
print y
