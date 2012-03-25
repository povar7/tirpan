'''
Created on 03.01.2012

@author: ramil
'''

class Scope(object):
    def __init__(self, parent = None, params_scope = False):
        self.parent = parent
        self.variables = {}
        self.params_scope = params_scope

    def add(self, var):
        var.parent = self
        self.variables[var.name] = var

    def find(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.find(name)
        return None

    def _getParamName(self, num):
        return 'param' + str(num)

    def addParam(self, num):
        from typegraph import VarTypeGraphNode
        var = VarTypeGraphNode(self._getParamName(num))
        var.setParamNumber(num)
        self.add(var)
        return var

    def findParam(self, num):
        return self.find(self._getParamName(num))

    def findOrAdd(self, name):
        res = self.find(name)
        if not res:
            from typegraph import VarTypeGraphNode
            res = VarTypeGraphNode(name)
            self.add(res)
        return res
 
    def getParent(self):
        return self.parent

    def printVariables(self):
        variables = sorted(self.variables.values(), \
                           lambda x, y: cmp((x.line, x.col), (y.line, y.col)))
        for var in variables:
            print var.name, ':', var.nodeType

    def linkParamsAndArgs(self, args):
        variables = sorted(self.variables.values(), \
                           lambda x, y: cmp(x.paramNumber, y.paramNumber))
        args_num  = len(args)
        for index in range(args_num):
            try:
                var = variables[index]
            except IndexError:
                return False
            var.nodeType = set([args[index]])
        vars_num  = len(variables)
        for index in range(args_num, vars_num):
            var = variables[index]
            if not var.defaultParam:
                return False
        return True 
