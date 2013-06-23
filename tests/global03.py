res1 = 0
res2 = 0

def foo():
    if 1 == 1:
        global res1
    res1, res2 = [True, 'abc']

foo()
