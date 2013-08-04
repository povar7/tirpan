import os
import const

def foo():
    global x, y, z
    for (x1, y1, z1) in os.walk(const.DIR_FOR_BUILTIN05):
        print x1, y1, z1
        x = x1
        y = y1
        z = z1

foo()
print x
print y
print z
