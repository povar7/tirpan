if True:
    d = [[1, 3.14]]
if True:
    d = {'foo': {'filename' : 'abc'}}

def foo():
    global x
    for key in d:
        x = d[key]['filename']

foo()
print x
