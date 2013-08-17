def foo(a, b):
    if cond:
        return a
    else:
        return b

tmp = [1]
x   = ['abc', tmp]
x   = 3.0
y   = tmp
y   = u'abc'
z   = foo(x, y)
x   = 7
