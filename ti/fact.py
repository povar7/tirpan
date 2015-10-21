class SimpleCondition(object):
    pass


class BooleanCondition(SimpleCondition):
    def __init__(self, cond, value):
        self.cond = cond
        self.value = value

class IsinstanceCondition(SimpleCondition):
    def __init__(self, variable, type):
        self.variable = variable
        self.type = type
