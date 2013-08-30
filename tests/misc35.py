d = {}
d[None] = 0
d['xx'] = 1
d[1234] = 2

for key in d:
    try:
        x = len(key)
    except TypeError:
        x = d['xx']
    print x

a = 1
