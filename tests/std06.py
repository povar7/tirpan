def foo():
    for i in [(1, 'abc'), (3.14, u'abc')]:
        yield i

def bar():
    global a, b
    for (a1, b1) in foo():
        print a1, b1
        a = a1
        b = b1

bar()
print
print a
print b
