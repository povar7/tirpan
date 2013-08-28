class A(object):
    pass

class B(A):
    def __init__(self):

        def trav(cls):
            """A traversal function to walk through all the classes in
            the inheritance tree. The return is a list of all the
            __signals__ dictionaries."""
        
            if '__signals__' in cls.__dict__:
                signal_list = [cls.__signals__]
            else:
                signal_list = []

            for base_cls in cls.__bases__:
                base_list = trav(base_cls)
                if len(base_list) > 0:
                    signal_list = signal_list + base_list

            return signal_list

        for s in trav(self.__class__):
            print s

x = B()
a = 1
