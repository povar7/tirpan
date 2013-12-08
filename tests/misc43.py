def foo(p):
    global x
    x = p

def recursive_action(item, func, *args):
    if isinstance(item, list):
        for sub_item in item[1:]:
            recursive_action(sub_item, func, *args)
        last_item = item[0]
    else:
        last_item = item
    func(last_item, *args)

a = [1, 3.14, 'abc']
recursive_action(a, foo)
print x
