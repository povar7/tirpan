def foo(x):
    global res
    res = x

foo(1)
foo(3.14)

res = None