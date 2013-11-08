def foo(a, b):
    if a < b:
        return a
    else:
        return b

tmp = [7]
if True:
    x = ['abc', tmp]
if True:
    x = 3.0
if True:
    y = tmp
if True:
    y = u'abc'
if True:
    z = foo(x, y)
if True:
    x = 1
