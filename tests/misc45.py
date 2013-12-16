import os

def foo(a = ''):
    os.path.basename(a)

def bar():
    foo([])

foo()
bar()
