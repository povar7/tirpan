'''
Created on 03.01.2012

@author: ramil
'''

from typenodes import *

def sort_params(x, y):
    if x.kwParam:
        return 1
    if y.kwParam:
        return -1
    if x.varParam:
        return 1
    if y.varParam:
        return -1
    return cmp(x.paramNumber, y.paramNumber)

class DummyWrap(object):
    def __init__(self, scope):
        self.scope = scope

class Scope(object):
    def __init__(self, parent = None, has_globals = False):
        self.parent = parent
        self.variables = {}
        self.has_globals = has_globals
        if self.has_globals:
            self.global_names = set() 

    def add(self, var):
        var.setParent(self)
        self.variables[var.name] = var

    def find(self, name, consider_globals = False, wrap_file_scope = None):
        if name in self.variables:
            return self.variables[name]
        if consider_globals and self.has_globals and name not in self.global_names:
            if wrap_file_scope:
                wrap_file_scope.scope = None
            return None
        if self.parent:
            return self.parent.find(name, consider_globals, wrap_file_scope)
        return None

    def findInScope(self, name):
        if name in self.variables:
            return self.variables[name]
        return None 

    def _getParamName(self, num):
        return 'param' + str(num)

    def addParam(self, num):
        from typegraph import UsualVarTypeGraphNode
        var = UsualVarTypeGraphNode(self._getParamName(num))
        var.setParamNumber(num)
        self.add(var)
        return var

    def findParam(self, num):
        return self.find(self._getParamName(num))

    def findOrAdd(self, name, consider_globals = False, file_scope = None):
        wrap_file_scope = DummyWrap(file_scope)
        res = self.find(name, consider_globals, wrap_file_scope)
        file_scope = wrap_file_scope.scope
        if not res:
            from typegraph import UsualVarTypeGraphNode
            res = UsualVarTypeGraphNode(name)
            if consider_globals and file_scope:
                file_scope.add(res)
            else:
                self.add(res)
        return res
 
    def getParent(self):
        return self.parent

    def printVariables(self):
        variables = sorted(self.variables.values(), \
                           lambda x, y: cmp((x.line, x.col), (y.line, y.col)))
        for var in variables:
            print var.name, ':', var.nodeType

    def getArgs(self, args, kwargs):
        variables = sorted(self.variables.values(), sort_params)
        args_num  = len(args)
        vars_num  = len(variables)
        var_index = 0
        arg_index = 0
        res       = []
        while True:
            if var_index >= vars_num:
                break
            var = variables[var_index]
            if var.defaultParam:
                if arg_index < args_num:
                    res.append(args[arg_index])
                    arg_index += 1
                else:
                    res.append(list(var.nodeType)[0])
                var_index += 1
                continue
            elif var.varParam:
                args_tuple = TypeTuple()
                while True:
                    if arg_index >= args_num:
                        break
                    args_tuple.add_elem(args[arg_index])
                    arg_index += 1
                res.append(args_tuple)
                var_index += 1
            elif var.kwParam:
                res.append(kwargs)
                var_index += 1
            else:
                if arg_index >= args_num:
                    return None
                res.append(args[arg_index])
                var_index += 1
                arg_index += 1
        if arg_index < args_num:
            return None
        return tuple(res)

    def linkParamsAndArgs(self, args):
        variables = sorted(self.variables.values(), sort_params)
        vars_num  = len(variables)
        for index in range(vars_num):
            var = variables[index]
            arg = args[index]
            var.nodeType = set([arg])

    def addGlobalNames(self, names):
        if not self.has_globals:
            self.parent.addGlobalNames(names)
        else:
            self.global_names = self.global_names.union(set(names))
