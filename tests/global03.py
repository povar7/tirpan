res1 = 1
res2 = 1

def foo():
    if 0 == 0:
        global res1
    res1, res2 = [True, 'abc']

foo()
