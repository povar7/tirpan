'''
Created on 03.01.2013

@author: bronikkk
'''

import ast

def check_exceptions(expr):
   from typegraph import ExternFuncDefTypeGraphNode
   from typenodes import TypeListOrTuple
   if not isinstance(expr, ast.Expr):
       return False
   func_call = expr.value
   if not isinstance(func_call, ast.Call):
       return False
   func_type = func_call.func.link.nodeType
   if all([isinstance(elem, ExternFuncDefTypeGraphNode) and elem.name in ['iter', 'extend'] for elem in func_type]):
       if len(func_call.args) != 1:
           return False
       else:
           arg = func_call.args[0]
           arg_type = arg.link.nodeType
           return len(arg_type) > 0 and all([isinstance(elem, TypeListOrTuple) for elem in arg_type])
   return False
