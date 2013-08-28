def foo(x):
    return chr(x + 32 if x >= ord('A') and x <= ord('Z') else x)

print foo(88)
a = 1
