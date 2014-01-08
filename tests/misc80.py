class GrampsType(object):
    def __init__(self, value=None):
        self.set(value)

    def __set_int(self, value):
        self.__value  = value
        self.__string = u''

    def __set_instance(self, value):
        self.__value  = value.value
        self.__string = value.string

    def set(self, value):
        if isinstance(value, int):
            self.__set_int(value)
        elif isinstance(value, self.__class__):
            self.__set_instance(value)

grampsType = GrampsType(1)
