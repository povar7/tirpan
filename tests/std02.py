a = {1: 3.14}
a['2'] = 6.28
print a
b = [1, 2, 3, 4, 5]
b[0:4:2] = [6, 7]
print b
c = [1, 2, 3, 4, 5]
c[0:4:2] = [6, 7.0]
print c
d = c[1:4]
print d
e = [1, 2]
f = e[:]
e[0] = 3.14
print e
print f
