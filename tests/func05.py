foo = 10

def foo(a, b):
    if cond:
        return a
    else:
        return b

tmp = [7]
x   = ['abc', tmp]
x   = 3.0
y   = tmp
y   = u'abc'
z   = foo(x, y)
x   = 1

foo = 3.14

def foo(a, b):
    return [a, b]

bar = foo

def bar(a, b):
    return 2j

u   = bar(x, y)
