'''
Created on 03.03.2012

@author: bronikkk
'''

import ast
from types import FunctionType

from typegraph import FuncDefTypeGraphNode
from typenodes import TypeNode, TypeAtom, TypeList, TypeTuple, TypeDict

class HitsCounter(object):
    def __init__(self):
        self.total  = 0
        self.hits   = 0
        self.misses = 0

    def assert_variable(self, name, cond):
        self.total += 1
        if cond:
            self.hits   += 1
        else:
            print "Miss: %s" % name
            self.misses += 1

    def __str__(self):
        return 'Total: %d, hits: %d, misses: %d' % (self.total, self.hits, self.misses)

counter = HitsCounter()
sandbox = {}

def insert_asserts(body, asserts):
    res = []
    for stmt in body:
        res.append(stmt)
        res += asserts
    return res

def check_type(var_type, var):
    try:
        if isinstance(var_type, TypeNode) and not var_type.has_type(type(var)):
            return False
        if isinstance(var_type, TypeAtom):
            return True
        elif isinstance(var_type, FuncDefTypeGraphNode):
            return isinstance(var, FunctionType) 
        elif isinstance(var_type, (TypeList, TypeTuple)):
            for elem in var:
                if not check_types(var_type.elems, elem):
                    return False
        elif isinstance(var_type, TypeDict):
            for key in var.keys():
                if not check_types(var_type.keys, key):
                    return False
            for val in var.values():
                if not check_types(var_type.vals, val):
                    return False
        return True
    except:
        return False

def check_types(var_types, var):
    for var_type in var_types:
        if check_type(var_type, var):
            return True
    return False

def check_variable(var, name, scope):
    real_var = scope.variables[name]
    cond = check_types(real_var.nodeType, var)
    counter.assert_variable(name, cond)

sandbox['check_variable'] = check_variable

def generate_asserts_list(variables):
    res = []
    for var in variables:
        func_call = ast.Expr(ast.Call(ast.Name('check_variable', ast.Load()), [ast.Name(var.name, ast.Load()), ast.Str(var.name), ast.Name('sandbox_scope', ast.Load())], [], None, None))
        stmt = ast.TryExcept([func_call], [ast.ExceptHandler(ast.Name('NameError', ast.Load()), None, [ast.Pass()])], [])
        stmt.lineno     = 0
        stmt.col_offset = 0
        ast.fix_missing_locations(stmt)
        res.append(stmt)
    return res

def insert_global_asserts(module, link):
    scope            = link.scope
    asserts          = generate_asserts_list(scope.variables.values())
    module.body      = insert_asserts(module.body, asserts)
    code             = compile(module, link.name, 'exec')

    sandbox['sandbox_scope'] = scope

    exec code in sandbox

def generate_asserts(module):
    insert_global_asserts(module, module.link)
    print counter
