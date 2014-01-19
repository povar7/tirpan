def func(p, *args, **kwargs):
    print p

args   = (1000000000000l,)
kwargs = {'foo' : 'bar'}
func(1, flag=args[0], *args, **kwargs)
