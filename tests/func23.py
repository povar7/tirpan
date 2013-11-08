a = 1

def foo(x):
    return (x, a)

if True:
    b = 'abc'
if True:
    b = u'abc'

z = foo(b)

if True:
    a = 3.14
