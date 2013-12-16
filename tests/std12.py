def foo():
    global x
    collection = {1, 3.14, 'abc'}
    for elem in collection:
        x = elem

foo()
print x
