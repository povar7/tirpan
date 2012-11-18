def foo(**kwargs):
    for el in kwargs:
        return el

x = foo(abc='value')
print x
