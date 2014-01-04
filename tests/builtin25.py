import random

if random.randint(0, 1):
    d = {'abc' : 1}
else:
    d = {'def' : 1}

x = d.has_key('abc')
print x
