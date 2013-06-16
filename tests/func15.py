def foo(x, y, z):
    return z

def bar(x, *args):
    return foo(x, *args)

a = bar(1, 'abc', 3.14)
print a
