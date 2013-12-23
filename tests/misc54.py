import sys

def foo():
    temp, sys.argv = sys.argv, sys.argv[:1]

foo()
a = 1
