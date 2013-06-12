foo = 10

def foo(a, b):
    return a
    return b

tmp = [1]
x   = ['abc', tmp]
x   = 3.0
y   = tmp
y   = u'abc'
z   = foo(x, y)
x   = 7

foo = 3.14

def foo(a, b):
    return [a, b]

bar = foo

def bar(a, b):
    return 2j

u   = bar(x, y)
