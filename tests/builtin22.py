from collections import defaultdict

d = {1: 3.14, 'abc': u'abc'}
item_hash = defaultdict(list)
for elem in d:
    item_hash[elem].append(d[elem])
x = item_hash
print x
