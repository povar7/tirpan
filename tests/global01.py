res = None

def foo(x):
    global res
    res = x

foo(1)
foo(3.14)
