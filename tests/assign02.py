def foo():
    global x
    elems = [1, 3.14, 'abc']
    for el in elems:
        x = el

foo()
print x
