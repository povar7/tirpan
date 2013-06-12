def foo(x, y = 1, *args):
    return args

x = foo(3, 6, 2.0, 'abc')
y = foo(3, 6, 2.0, 'abc', 7.0)
