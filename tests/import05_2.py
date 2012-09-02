data = True

def foo(t = [1, 2, 3]):
    global data
    for elem in t:
        print elem
        data = elem
