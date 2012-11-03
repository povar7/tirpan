class A:
    def __init__(self):
        pass

    def reg_plugins(self, direct, dbstate=None, uistate=None,
                    append=True, load_on_reg=False):
        return True

a = A()
x = a.reg_plugins('plugins')
print x
