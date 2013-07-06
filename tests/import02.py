from sys import argv
from sys import path as mama
from sys import getsizeof

def foo():
    return argv[0]

def bar():
    return mama

x = foo()
print x
y = bar()
print y
z = getsizeof('abc')
print z
t = getsizeof('abc', 100)
print t
